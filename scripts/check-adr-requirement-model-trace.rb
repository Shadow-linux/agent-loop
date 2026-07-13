#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "pathname"
require "set"

unless (3..4).cover?(ARGV.length)
  abort "usage: #{$PROGRAM_NAME} REQUIREMENT_README EFFECTIVE_SOURCE DECISION [WORKSPACE_ROOT]"
end

readme_path, source_path, decision_path = ARGV.first(3).map { |path| File.expand_path(path) }
workspace_root = File.expand_path(ARGV[3] || File.dirname(readme_path))

MODEL_ID_PATTERN = /\A(?:REL|PERM|CMD|EVT|FLOW|STATE|PM|EX)-[A-Z0-9-]+\z/
CONCEPT_ID_PATTERN = /\AC-[A-Z0-9-]+\z/
SLICE_ID_PATTERN = /\ADS-[A-Z0-9-]+\z/

REQUIRED_GATE_ITEMS = [
  "Effective Concept Source resolves and matches the reviewed source",
  "Concept Foundation Status is accepted or reasoned `concept-foundation-not-needed`",
  "Upstream Compatibility is `current`",
  "Every source Requirement Model ID has an explicit scope disposition, or trace is reasoned not-applicable",
  "Every in-scope Accepted Requirement Model ID has exactly one disposition",
  "Every `landed` row has Technical Landing, Preserved Invariant, Design Slice, and Verification",
  "Every `covered-by-accepted-decision` and `feature-local` row names an existing or explicitly planned verified owner path",
  "Every `not-applicable`, deferred, and out-of-scope item is visible in Human Review Summary",
  "Every implementation-bearing technical rule is represented in Design Slice Coverage",
  "No required Design Slice is `unassigned`",
  "No unresolved product-semantic blocker remains"
].freeze

REQUIRED_OPERATIONAL_CONCERNS = [
  "Migration / Backfill",
  "Compatibility",
  "Rollout / Cutover",
  "Rollback / Reversibility"
].freeze

def read_file(path)
  abort "missing file: #{path}" unless File.file?(path)

  File.read(path)
end

def metadata(content, label)
  match = content.match(/^#{Regexp.escape(label)}:\s*(.*?)\s*$/)
  match && match[1].strip
end

def optional_section(content, title, level: 2)
  marker = "#" * level
  stop_marker = Regexp.escape("#") + "{1," + level.to_s + "}"
  pattern = Regexp.new(
    "^#{Regexp.escape(marker)} #{Regexp.escape(title)}\\s*$\\n(.*?)(?=^#{stop_marker}\\s|\\z)",
    Regexp::MULTILINE
  )
  match = content.match(pattern)
  match && match[1]
end

def section(content, title, level: 2)
  value = optional_section(content, title, level: level)
  abort "missing section: #{"#" * level} #{title}" unless value

  value
end

def split_row(line)
  line.strip.sub(/^\|/, "").sub(/\|$/, "").split("|").map(&:strip)
end

def table(content, title, level: 2)
  lines = section(content, title, level: level).lines.map(&:strip)
  start = lines.index { |line| line.start_with?("|") }
  abort "missing table in section: #{title}" unless start

  table_lines = lines.drop(start).take_while { |line| line.start_with?("|") }
  abort "incomplete table in section: #{title}" if table_lines.length < 3

  headers = split_row(table_lines[0])
  rows = table_lines.drop(2).map do |line|
    cells = split_row(line)
    abort "column count mismatch in section: #{title}" unless cells.length == headers.length

    headers.zip(cells).to_h
  end
  abort "empty table in section: #{title}" if rows.empty?

  rows
end

def normalized(value)
  value.to_s.strip.gsub(/\A`|`\z/, "")
end

def concrete?(value)
  text = normalized(value)
  return false if text.empty?
  return false if text.match?(/\A(?:-|none|n\/a|na|not applicable|tbd|todo|unknown)\z/i)
  return false if text.match?(/<[^>]+>/)

  true
end

def concrete_reason?(value)
  text = normalized(value)
  concrete?(text) && text.length >= 12
end

def assert_unique!(values, context)
  duplicates = values.group_by(&:itself).select { |_value, rows| rows.length > 1 }.keys
  abort "duplicate IDs in #{context}: #{duplicates.sort.join(', ')}" unless duplicates.empty?
end

def parse_id_list(value, pattern, context, allow_none: false)
  text = value.to_s.strip
  return [] if allow_none && text.casecmp("none").zero?
  abort "#{context} is missing" if text.empty?

  tokens = text.split(",").map { |token| normalized(token) }
  invalid = tokens.reject { |token| token.match?(pattern) }
  abort "invalid values in #{context}: #{invalid.join(', ')}" unless invalid.empty?
  assert_unique!(tokens, context)
  tokens
end

def parse_date!(value, context)
  abort "#{context} is missing" unless concrete?(value)

  Date.iso8601(value)
rescue Date::Error
  abort "#{context} must be YYYY-MM-DD"
end

def confined_path(root, relative)
  root_path = Pathname.new(root).cleanpath
  candidate = Pathname.new(File.expand_path(relative, root)).cleanpath
  prefix = root_path.to_s.end_with?(File::SEPARATOR) ? root_path.to_s : root_path.to_s + File::SEPARATOR
  abort "reference escapes workspace root: #{relative}" unless candidate.to_s.start_with?(prefix)

  candidate.to_s
end

def markdown_path(value)
  normalized(value)[/([A-Za-z0-9._\/-]+\.md)\b/, 1]
end

def validate_decision_reference!(value, workspace_root, context, allow_planned: false, allowed_statuses: ["accepted"])
  planned = normalized(value).start_with?("planned:")
  abort "#{context} cannot be planned" if planned && !allow_planned
  path = markdown_path(value)
  abort "#{context} must name a decision Markdown path" unless path
  absolute = confined_path(workspace_root, path)
  return if planned

  content = read_file(absolute)
  status = metadata(content, "Status")
  unless allowed_statuses.include?(status)
    abort "#{context} decision status must be #{allowed_statuses.join(' or ')}"
  end
end

def validate_feature_reference!(value, workspace_root, context)
  planned = normalized(value).start_with?("planned:")
  path = markdown_path(value)
  abort "#{context} must name a Feature Spec path" unless path&.match?(%r{(?:^|/)features/[^/]+/spec\.md\z})
  absolute = confined_path(workspace_root, path)
  return if planned

  content = read_file(absolute)
  status = metadata(content, "Status")
  abort "#{context} Feature Spec must be proposed or accepted" unless %w[proposed accepted].include?(status)
end

def validate_human_review!(decision, decision_status)
  return if decision_status == "proposed"

  review = section(decision, "Human Review Evidence")
  abort "accepted ADR must record Decision: accepted" unless metadata(review, "Decision") == "accepted"
  abort "accepted ADR must record who confirmed it" unless concrete?(metadata(review, "Confirmed By"))
  parse_date!(metadata(review, "Confirmed At"), "Human Review Confirmed At")
  abort "accepted ADR must record Human Review evidence" unless concrete_reason?(metadata(review, "Evidence"))
end

def validate_gate!(decision)
  gate = section(decision, "Coverage Hard Gate")
  unchecked = gate.lines.grep(/^\s*- \[ \]/)
  abort "Coverage Hard Gate contains unchecked items" unless unchecked.empty?

  completed = gate.lines.map do |line|
    match = line.match(/^\s*- \[[xX]\]\s+(.+?)\s*$/)
    match && match[1]
  end.compact
  assert_unique!(completed, "Coverage Hard Gate")
  missing = REQUIRED_GATE_ITEMS - completed
  abort "Coverage Hard Gate is missing required items: #{missing.join('; ')}" unless missing.empty?
  extra = completed - REQUIRED_GATE_ITEMS
  abort "Coverage Hard Gate contains unsupported items: #{extra.join('; ')}" unless extra.empty?
end

def validate_operational!(decision)
  rows = table(decision, "Operational Landing Trigger Assessment")
  concerns = rows.map { |row| row.fetch("Concern", "") }
  assert_unique!(concerns, "Operational Landing Trigger Assessment")
  missing = REQUIRED_OPERATIONAL_CONCERNS - concerns
  extra = concerns - REQUIRED_OPERATIONAL_CONCERNS
  abort "operational concern inventory mismatch; missing=#{missing.join(', ')} extra=#{extra.join(', ')}" unless missing.empty? && extra.empty?

  triggered_details = []
  rows.each do |row|
    concern = row.fetch("Concern", "")
    status = row.fetch("Status", "")
    reason = row.fetch("Reason / Trigger Evidence", "")
    detail = row.fetch("Detail Section If Triggered", "")
    abort "invalid operational trigger status for #{concern}" unless %w[triggered not-triggered].include?(status)
    abort "operational trigger #{concern} needs a concrete reason" unless concrete_reason?(reason)

    if status == "triggered"
      abort "triggered operational concern #{concern} needs a detail section" unless concrete?(detail)
      triggered_details << detail
    elsif !normalized(detail).casecmp("none").zero?
      abort "not-triggered operational concern #{concern} must use Detail Section: none"
    end
  end

  operational = optional_section(decision, "Triggered Operational Landing")
  if triggered_details.empty?
    abort "Triggered Operational Landing must be absent when no concern is triggered" if operational
    return
  end

  abort "Triggered Operational Landing is missing" unless operational
  triggered_details.each do |detail|
    abort "missing triggered operational detail heading: #{detail}" unless decision.match?(/^### #{Regexp.escape(detail)}\s*$/)
  end
end

readme = read_file(readme_path)
source = read_file(source_path)
decision = read_file(decision_path)

pointer = section(readme, "Effective Concept Foundation")
pointer_status = metadata(pointer, "Status")
pointer_source = metadata(pointer, "Effective Source")
abort "effective source pointer is missing" unless concrete?(pointer_source)

resolved_source = File.expand_path(pointer_source, File.dirname(readme_path))
unless Pathname.new(resolved_source).cleanpath == Pathname.new(source_path).cleanpath
  abort "effective source pointer does not resolve to supplied source"
end

source_status = metadata(source, "Concept Foundation Status")
allowed_source_statuses = %w[accepted concept-foundation-not-needed]
unless allowed_source_statuses.include?(pointer_status) && source_status == pointer_status
  abort "effective Concept Foundation must be accepted or reasoned not-needed and statuses must align"
end

decision_status = metadata(decision, "Status")
abort "decision status must be proposed or accepted for gate validation" unless %w[proposed accepted].include?(decision_status)
decision_id = decision[/^#\s+(ADR-[A-Z0-9-]+):/, 1]
abort "decision heading must declare an ADR ID" unless decision_id
validate_human_review!(decision, decision_status)

snapshot = section(decision, "Effective Requirement Snapshot")
snapshot_source = metadata(snapshot, "Effective Concept Source")
snapshot_status = metadata(snapshot, "Concept Foundation Status")
compatibility = metadata(snapshot, "Upstream Compatibility")
last_check = metadata(snapshot, "Last Compatibility Check")

abort "ADR Effective Concept Source does not match requirement pointer" unless snapshot_source == pointer_source
abort "ADR Concept Foundation status does not match effective source" unless snapshot_status == source_status
abort "Upstream Compatibility must be current before acceptance" unless compatibility == "current"
parse_date!(last_check, "Last Compatibility Check")

slice_rows = table(decision, "Design Slice Coverage")
slice_values = slice_rows.map { |row| row.fetch("Design Slice ID", "") }
invalid_slices = slice_values.reject { |value| value.match?(SLICE_ID_PATTERN) }
abort "invalid Design Slice IDs: #{invalid_slices.join(', ')}" unless invalid_slices.empty?
assert_unique!(slice_values, "Design Slice Coverage")
allowed_slice_statuses = %w[planned implemented verified deferred out-of-scope]
slice_statuses = {}
slice_rows.each do |row|
  slice_id = row.fetch("Design Slice ID", "")
  capability = row.fetch("Required Capability / Rule", "")
  owner = row.fetch("Owning Feature(s)", "")
  verification = row.fetch("Verification", "")
  status = row.fetch("Coverage Status", "")
  abort "Design Slice #{slice_id} has no required capability" unless concrete_reason?(capability)
  abort "Design Slice #{slice_id} has no owner" unless concrete?(owner)
  abort "Design Slice #{slice_id} has no verification" unless concrete?(verification)
  abort "Design Slice #{slice_id} has invalid coverage status: #{status}" unless allowed_slice_statuses.include?(status)
  slice_statuses[slice_id] = status
end

validate_gate!(decision)
validate_operational!(decision)

if source_status == "concept-foundation-not-needed"
  reason = metadata(source, "Not-Needed Reason")
  abort "concept-foundation-not-needed requires a concrete reason" unless concrete_reason?(reason)

  concepts = parse_id_list(metadata(snapshot, "Accepted Concept IDs"), CONCEPT_ID_PATTERN, "ADR Accepted Concept IDs", allow_none: true)
  models = parse_id_list(metadata(snapshot, "Accepted Requirement Model IDs"), MODEL_ID_PATTERN, "ADR Accepted Requirement Model IDs", allow_none: true)
  abort "reasoned not-needed ADR must not declare Concept IDs" unless concepts.empty?
  abort "reasoned not-needed ADR must not declare Requirement Model IDs" unless models.empty?
  abort "reasoned not-needed ADR must set Trace Applicability: not-applicable" unless metadata(snapshot, "Trace Applicability") == "not-applicable"
  trace_reason = metadata(snapshot, "Trace Not-Applicable Reason")
  abort "reasoned not-needed ADR needs a concrete trace reason" unless concrete_reason?(trace_reason)

  puts "PASS: reasoned concept-foundation-not-needed ADR #{decision_status} gate is complete"
  exit 0
end

abort "accepted Concept Foundation ADR must set Trace Applicability: required" unless metadata(snapshot, "Trace Applicability") == "required"

concept_rows = table(source, "Concept Definitions")
source_concept_values = concept_rows.map { |row| row.fetch("Concept ID", "") }
assert_unique!(source_concept_values, "source Concept Definitions")
source_concepts = source_concept_values.to_set
unless source_concepts.all? { |value| value.match?(CONCEPT_ID_PATTERN) }
  abort "source Concept Definitions contains invalid IDs"
end

model_tables = {
  "Concept Relationships" => ["Relationship ID", /\AREL-[A-Z0-9-]+\z/],
  "Role / Permission Matrix" => ["Permission Rule ID", /\APERM-[A-Z0-9-]+\z/],
  "Commands / Events" => ["Action ID", /\A(?:CMD|EVT)-[A-Z0-9-]+\z/],
  "Primary Business Flow" => ["Flow Step ID", /\AFLOW-[A-Z0-9-]+\z/],
  "Product State Model" => ["State Model ID", /\ASTATE-[A-Z0-9-]+\z/],
  "Requirement Product Model" => ["Product Model ID", /\APM-[A-Z0-9-]+\z/],
  "Exception Paths" => ["Scenario ID", /\AEX-[A-Z0-9-]+\z/]
}

source_model_values = model_tables.flat_map do |title, (column, pattern)|
  values = table(source, title).map { |row| row.fetch(column, "") }
  assert_unique!(values, "source #{title}")
  abort "source #{title} contains invalid IDs" unless values.all? { |value| value.match?(pattern) }
  values
end
assert_unique!(source_model_values, "accepted Requirement Model")
source_models = source_model_values.to_set

snapshot_concept_values = parse_id_list(
  metadata(snapshot, "Accepted Concept IDs"),
  CONCEPT_ID_PATTERN,
  "ADR Accepted Concept IDs"
)
snapshot_model_values = parse_id_list(
  metadata(snapshot, "Accepted Requirement Model IDs"),
  MODEL_ID_PATTERN,
  "ADR Accepted Requirement Model IDs"
)
snapshot_concepts = snapshot_concept_values.to_set
snapshot_models = snapshot_model_values.to_set
abort "ADR scope must name accepted Concept IDs" if snapshot_concepts.empty?
abort "ADR scope must name accepted Requirement Model IDs" if snapshot_models.empty?

unknown_concepts = snapshot_concepts - source_concepts
abort "ADR snapshot contains unknown Concept IDs: #{unknown_concepts.to_a.sort.join(', ')}" unless unknown_concepts.empty?
unknown_models = snapshot_models - source_models
abort "ADR snapshot contains unknown Requirement Model IDs: #{unknown_models.to_a.sort.join(', ')}" unless unknown_models.empty?

scope_rows = table(decision, "Requirement Model Scope Inventory")
scope_ref_values = scope_rows.map { |row| row.fetch("Requirement Model Ref", "") }
assert_unique!(scope_ref_values, "Requirement Model Scope Inventory")
scope_refs = scope_ref_values.to_set
missing_scope = source_models - scope_refs
extra_scope = scope_refs - source_models
unless missing_scope.empty? && extra_scope.empty?
  abort "Requirement Model Scope Inventory mismatch; missing=#{missing_scope.to_a.sort.join(', ')} extra=#{extra_scope.to_a.sort.join(', ')}"
end

allowed_scope_dispositions = %w[in-scope covered-by-accepted-decision feature-local proposed-decision not-applicable]
in_scope = Set.new
scope_rows.each do |row|
  ref = row.fetch("Requirement Model Ref", "")
  disposition = row.fetch("Scope Disposition", "")
  owner = row.fetch("Owner / Reason", "")
  abort "scope row #{ref} has invalid disposition: #{disposition}" unless allowed_scope_dispositions.include?(disposition)
  case disposition
  when "in-scope"
    in_scope << ref
    unless [decision_id, "this ADR"].include?(normalized(owner))
      abort "in-scope model #{ref} must name #{decision_id} or this ADR"
    end
  when "covered-by-accepted-decision"
    validate_decision_reference!(owner, workspace_root, "scope row #{ref}")
  when "feature-local"
    validate_feature_reference!(owner, workspace_root, "scope row #{ref}")
  when "proposed-decision"
    validate_decision_reference!(
      owner,
      workspace_root,
      "scope row #{ref}",
      allow_planned: true,
      allowed_statuses: ["proposed"]
    )
  when "not-applicable"
    reason = owner.sub(/\Areason:\s*/i, "")
    abort "scope row #{ref} needs a concrete not-applicable reason" unless owner.match?(/\Areason:/i) && concrete_reason?(reason)
  end
end
abort "ADR Accepted Requirement Model IDs must equal in-scope inventory IDs" unless snapshot_models == in_scope

trace_rows = table(decision, "Requirement Model Technical Landing Trace")
trace_ref_values = trace_rows.map { |row| row.fetch("Requirement Model Ref", "") }
assert_unique!(trace_ref_values, "Requirement Model Technical Landing Trace")
trace_refs = trace_ref_values.to_set
missing_rows = snapshot_models - trace_refs
extra_rows = trace_refs - snapshot_models
abort "missing trace coverage: #{missing_rows.to_a.sort.join(', ')}" unless missing_rows.empty?
abort "trace rows outside declared ADR scope: #{extra_rows.to_a.sort.join(', ')}" unless extra_rows.empty?

allowed_dispositions = %w[landed covered-by-accepted-decision feature-local not-applicable]
landed_rows = []
trace_rows.each do |row|
  ref = row.fetch("Requirement Model Ref", "")
  meaning = row.fetch("Accepted Meaning / Constraint", "")
  disposition = row.fetch("Disposition", "")
  abort "trace row #{ref} has no accepted meaning/constraint reference" unless concrete_reason?(meaning)
  abort "trace row #{ref} has invalid disposition: #{disposition}" unless allowed_dispositions.include?(disposition)

  landing = row.fetch("Technical Landing", "")
  invariant = row.fetch("Preserved Invariant", "")
  slice = row.fetch("Design Slice", "")
  verification = row.fetch("Verification", "")

  case disposition
  when "landed"
    required = {
      "Technical Landing" => landing,
      "Preserved Invariant" => invariant,
      "Design Slice" => slice,
      "Verification" => verification
    }
    missing = required.reject { |_field, value| concrete?(value) }.keys
    abort "landed trace row #{ref} has empty fields: #{missing.join(', ')}" unless missing.empty?
    landed_rows << row
  when "covered-by-accepted-decision"
    validate_decision_reference!(landing, workspace_root, "trace row #{ref}")
    abort "covered-by-accepted-decision trace row #{ref} must name verification direction" unless concrete_reason?(verification)
  when "feature-local"
    validate_feature_reference!(landing, workspace_root, "trace row #{ref}")
    abort "feature-local trace row #{ref} must name verification direction" unless concrete_reason?(verification)
  when "not-applicable"
    reason = landing.sub(/\Areason:\s*/i, "")
    abort "not-applicable trace row #{ref} must give a concrete reason" unless landing.match?(/\Areason:/i) && concrete_reason?(reason)
  end
end

landed_rows.each do |row|
  slice_ids = parse_id_list(row.fetch("Design Slice", ""), SLICE_ID_PATTERN, "trace Design Slice IDs")
  unknown_slices = slice_ids.to_set - slice_statuses.keys.to_set
  abort "trace references unknown Design Slices: #{unknown_slices.to_a.sort.join(', ')}" unless unknown_slices.empty?
end

puts "PASS: ADR #{decision_status} technical landing trace covers #{snapshot_models.length} in-scope requirement-model IDs with #{landed_rows.length} landed rows"
