#!/usr/bin/env ruby
# frozen_string_literal: true

require "set"

abort "usage: #{$PROGRAM_NAME} REQUIREMENT PRODUCT SPEC" unless ARGV.length == 3

requirement_path, product_path, spec_path = ARGV

def read_file(path)
  abort "missing file: #{path}" unless File.file?(path)

  File.read(path)
end

def metadata(content, label)
  match = content.match(/^#{Regexp.escape(label)}:\s*(.+?)\s*$/)
  match && match[1].strip
end

def section(content, title, level: 2)
  marker = "#" * level
  stop_marker = Regexp.escape("#") + "{1," + level.to_s + "}"
  pattern = Regexp.new(
    "^#{Regexp.escape(marker)} #{Regexp.escape(title)}\\s*$\\n(.*?)(?=^#{stop_marker}\\s|\\z)",
    Regexp::MULTILINE
  )
  match = content.match(pattern)
  abort "missing section: #{marker} #{title}" unless match

  match[1]
end

def split_row(line)
  line.strip.sub(/^\|/, "").sub(/\|$/, "").split("|").map(&:strip)
end

def table(content, title, level: 2)
  raw_lines = section(content, title, level: level).lines.map(&:strip)
  table_start = raw_lines.index { |line| line.start_with?("|") }
  abort "missing table in section: #{title}" unless table_start

  lines = raw_lines.drop(table_start).take_while { |line| line.start_with?("|") }
  abort "missing table in section: #{title}" if lines.length < 3

  headers = split_row(lines[0])
  rows = lines.drop(2).map do |line|
    cells = split_row(line)
    abort "column count mismatch in section: #{title}" unless cells.length == headers.length

    headers.zip(cells).to_h
  end
  abort "empty table in section: #{title}" if rows.empty?

  rows
end

def ids(text, pattern)
  text.to_s.scan(pattern).to_set
end

def assert_defined!(used, defined, context)
  missing = used - defined
  abort "undefined IDs in #{context}: #{missing.to_a.sort.join(', ')}" unless missing.empty?
end

def assert_unique_ids!(values, context, pattern)
  invalid = values.reject { |value| value.match?(pattern) }
  abort "invalid IDs in #{context}: #{invalid.uniq.sort.join(', ')}" unless invalid.empty?

  duplicates = values.group_by(&:itself).select { |_value, rows| rows.length > 1 }.keys
  abort "duplicate IDs in #{context}: #{duplicates.sort.join(', ')}" unless duplicates.empty?
end

def assert_confirmed!(used, confirmed, context)
  unconfirmed = used - confirmed
  abort "unconfirmed Concept IDs in #{context}: #{unconfirmed.to_a.sort.join(', ')}" unless unconfirmed.empty?
end

def reject_placeholders!(content, path)
  placeholders = ["<topic>", "C-EXAMPLE", "C-OTHER", "TBD", "TODO", "待补充"]
  found = placeholders.select { |placeholder| content.include?(placeholder) }
  abort "placeholder content in #{path}: #{found.join(', ')}" unless found.empty?
end

requirement = read_file(requirement_path)
product = read_file(product_path)
spec = read_file(spec_path)

[requirement, product, spec].zip(ARGV).each { |content, path| reject_placeholders!(content, path) }

status = metadata(requirement, "Concept Foundation Status")
allowed = %w[accepted concept-foundation-not-needed]
abort "Concept Foundation must be accepted or reasoned not-needed, got: #{status || 'missing'}" unless allowed.include?(status)

product_status = metadata(product, "Concept Foundation Status")
spec_status = metadata(spec, "Concept Foundation Status")
abort "product Concept Foundation status mismatch" unless product_status == status
abort "spec Concept Foundation status mismatch" unless spec_status == status

product_effective_source = metadata(product, "Effective Concept Source")
spec_effective_source = metadata(spec, "Effective Concept Source")
abort "product Effective Concept Source is missing" if product_effective_source.to_s.empty?
abort "spec Effective Concept Source is missing" if spec_effective_source.to_s.empty?
abort "effective Concept Foundation source mismatch" unless product_effective_source == spec_effective_source

if status == "concept-foundation-not-needed"
  reason = metadata(requirement, "Not-Needed Reason")
  placeholders = ["n/a", "na", "none", "not applicable", "unknown", "tbd", "todo"]
  normalized_reason = reason.to_s.strip.downcase
  if reason.nil? || reason.strip.length < 12 || placeholders.include?(normalized_reason)
    abort "concept-foundation-not-needed requires a concrete reason"
  end
  puts "PASS: reasoned concept-foundation-not-needed trace"
  exit 0
end

required_order = [
  "## Concept Foundation",
  "## Concept Definitions",
  "## Concept Relationships",
  "## Role / Permission Matrix",
  "## Commands / Events",
  "## Primary Business Flow",
  "## Product State Model",
  "## Requirement Product Model",
  "## Exception Paths",
  "## Concept-To-Product Traceability"
]
positions = required_order.map do |heading|
  position = requirement.index(heading)
  abort "missing required heading: #{heading}" unless position
  position
end
abort "requirement product sections are out of order" unless positions == positions.sort

candidate_rows = table(requirement, "Concept Candidate Inventory")
candidate_id_values = candidate_rows.map { |row| row.fetch("Concept ID", "") }
assert_unique_ids!(candidate_id_values, "Concept Candidate Inventory", /\AC-[A-Z0-9-]+\z/)
candidate_ids = candidate_id_values.to_set

concept_rows = table(requirement, "Concept Definitions")
concept_id_values = concept_rows.map { |row| row.fetch("Concept ID", "") }
assert_unique_ids!(concept_id_values, "Concept Definitions", /\AC-[A-Z0-9-]+\z/)
concept_ids = concept_id_values.to_set
assert_defined!(concept_ids, candidate_ids, "Concept Definitions inventory")

canonical_names = concept_rows.to_h do |row|
  [row.fetch("Concept ID", ""), row.fetch("Canonical Name", "")]
end
abort "Concept Definitions contains empty Canonical Name" if canonical_names.values.any?(&:empty?)

confirmed = ids(section(requirement, "Human Confirmation", level: 3), /\bC-[A-Z0-9-]+\b/)
assert_defined!(confirmed, concept_ids, "Human Confirmation")
abort "Human Confirmation must name accepted Concept IDs" if confirmed.empty?

candidate_status = candidate_rows.to_h do |row|
  [row.fetch("Concept ID", ""), row.fetch("Status", "")]
end
not_accepted = confirmed.reject { |concept_id| candidate_status.fetch(concept_id, "") == "accepted" }
abort "Human Confirmation includes non-accepted inventory IDs: #{not_accepted.to_a.sort.join(', ')}" unless not_accepted.empty?

ambiguity_rows = table(requirement, "Blocking Ambiguities", level: 3)
open_ambiguities = ambiguity_rows.reject do |row|
  %w[resolved not-applicable].include?(row.fetch("Status", "").downcase)
end
abort "Blocking Ambiguities contains unresolved rows" unless open_ambiguities.empty?

relationship_rows = table(requirement, "Concept Relationships")
relationship_id_values = relationship_rows.map { |row| row.fetch("Relationship ID", "") }
assert_unique_ids!(relationship_id_values, "Concept Relationships", /\AREL-[A-Z0-9-]+\z/)
relationship_ids = relationship_id_values.to_set
relationship_concepts = relationship_rows.flat_map do |row|
  [row.fetch("From Concept ID", ""), row.fetch("To Concept ID", "")]
end.to_set
assert_defined!(relationship_concepts, concept_ids, "Concept Relationships")
assert_confirmed!(relationship_concepts, confirmed, "Concept Relationships")

role_rows = table(requirement, "Role / Permission Matrix")
permission_id_values = role_rows.map { |row| row.fetch("Permission Rule ID", "") }
assert_unique_ids!(permission_id_values, "Role / Permission Matrix", /\APERM-[A-Z0-9-]+\z/)
permission_ids = permission_id_values.to_set
role_concepts = role_rows.flat_map do |row|
  [row.fetch("Role Concept ID", ""), row.fetch("Product Object Concept ID", "")]
end.to_set
assert_defined!(role_concepts, concept_ids, "Role / Permission Matrix")
assert_confirmed!(role_concepts, confirmed, "Role / Permission Matrix")
permission_pairs = role_rows.map do |row|
  [row.fetch("Role Concept ID", ""), row.fetch("Product Object Concept ID", "")]
end.to_set

action_rows = table(requirement, "Commands / Events")
action_id_values = action_rows.map { |row| row.fetch("Action ID", "") }
assert_unique_ids!(action_id_values, "Commands / Events", /\A(?:CMD|EVT)-[A-Z0-9-]+\z/)
action_ids = action_id_values.to_set
action_concepts = action_rows.flat_map do |row|
  ids(row.fetch("Actor / Producer Concept ID", ""), /\bC-[A-Z0-9-]+\b/).to_a +
    ids(row.fetch("Target Concept ID", ""), /\bC-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(action_concepts, concept_ids, "Commands / Events")
assert_confirmed!(action_concepts, confirmed, "Commands / Events")
action_pairs = action_rows.map do |row|
  [row.fetch("Actor / Producer Concept ID", ""), row.fetch("Target Concept ID", "")]
end.to_set
missing_permissions = action_pairs - permission_pairs
unless missing_permissions.empty?
  rendered = missing_permissions.to_a.sort.map { |actor, target| "#{actor}->#{target}" }
  abort "Commands / Events missing Role / Permission Matrix pairs: #{rendered.join(', ')}"
end
action_actors = action_rows.to_h do |row|
  [row.fetch("Action ID", ""), row.fetch("Actor / Producer Concept ID", "")]
end

flow_rows = table(requirement, "Primary Business Flow")
flow_id_values = flow_rows.map { |row| row.fetch("Flow Step ID", "") }
assert_unique_ids!(flow_id_values, "Primary Business Flow", /\AFLOW-[A-Z0-9-]+\z/)
flow_ids = flow_id_values.to_set
flow_concepts = flow_rows.flat_map do |row|
  ids(row.values.join(" "), /\bC-[A-Z0-9-]+\b/).to_a
end.to_set
flow_actions = flow_rows.flat_map do |row|
  ids(row.values.join(" "), /\b(?:CMD|EVT)-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(flow_concepts, concept_ids, "Primary Business Flow")
assert_confirmed!(flow_concepts, confirmed, "Primary Business Flow")
assert_defined!(flow_actions, action_ids, "Primary Business Flow actions")
flow_rows.each do |row|
  action_id = row.fetch("Action ID", "")
  actor_id = row.fetch("Actor Concept ID", "")
  expected_actor = action_actors.fetch(action_id, nil)
  abort "Primary Business Flow actor mismatch for #{action_id}" unless expected_actor == actor_id
end

state_rows = table(requirement, "Product State Model")
state_id_values = state_rows.map { |row| row.fetch("State Model ID", "") }
assert_unique_ids!(state_id_values, "Product State Model", /\ASTATE-[A-Z0-9-]+\z/)
state_ids = state_id_values.to_set
state_concepts = state_rows.flat_map do |row|
  ids(row.values.join(" "), /\bC-[A-Z0-9-]+\b/).to_a
end.to_set
state_actions = state_rows.flat_map do |row|
  ids(row.values.join(" "), /\b(?:CMD|EVT)-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(state_concepts, concept_ids, "Product State Model")
assert_confirmed!(state_concepts, confirmed, "Product State Model")
assert_defined!(state_actions, action_ids, "Product State Model actions")

product_model_rows = table(requirement, "Requirement Product Model")
product_model_id_values = product_model_rows.map { |row| row.fetch("Product Model ID", "") }
assert_unique_ids!(product_model_id_values, "Requirement Product Model", /\APM-[A-Z0-9-]+\z/)
product_model_ids = product_model_id_values.to_set
product_model_concepts = product_model_rows.flat_map do |row|
  ids(row.fetch("Concept IDs", ""), /\bC-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(product_model_concepts, concept_ids, "Requirement Product Model")
assert_confirmed!(product_model_concepts, confirmed, "Requirement Product Model")

exception_rows = table(requirement, "Exception Paths")
exception_id_values = exception_rows.map { |row| row.fetch("Scenario ID", "") }
assert_unique_ids!(exception_id_values, "Exception Paths", /\AEX-[A-Z0-9-]+\z/)
exception_ids = exception_id_values.to_set
exception_concepts = exception_rows.flat_map do |row|
  ids(row.fetch("Concept / State / Action IDs", ""), /\bC-[A-Z0-9-]+\b/).to_a
end.to_set
exception_states = exception_rows.flat_map do |row|
  ids(row.fetch("Concept / State / Action IDs", ""), /\bSTATE-[A-Z0-9-]+\b/).to_a
end.to_set
exception_actions = exception_rows.flat_map do |row|
  ids(row.fetch("Concept / State / Action IDs", ""), /\b(?:CMD|EVT)-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(exception_concepts, concept_ids, "Exception Paths concepts")
assert_confirmed!(exception_concepts, confirmed, "Exception Paths concepts")
assert_defined!(exception_states, state_ids, "Exception Paths states")
assert_defined!(exception_actions, action_ids, "Exception Paths actions")

trace_rows = table(requirement, "Concept-To-Product Traceability")
trace_id_values = trace_rows.map { |row| row.fetch("Trace ID", "") }
assert_unique_ids!(trace_id_values, "Concept-To-Product Traceability", /\ATRACE-[A-Z0-9-]+\z/)
trace_concepts = trace_rows.flat_map do |row|
  ids(row.fetch("Accepted Concept IDs", ""), /\bC-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(trace_concepts, concept_ids, "Concept-To-Product Traceability")
assert_confirmed!(trace_concepts, confirmed, "Concept-To-Product Traceability")

defined_model_ids = relationship_ids | permission_ids | action_ids | flow_ids | state_ids | product_model_ids | exception_ids
trace_models = trace_rows.flat_map do |row|
  ids(row.fetch("Derived Model IDs / Sections", ""), /\b(?:REL|PERM|CMD|EVT|FLOW|STATE|PM|EX)-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(trace_models, defined_model_ids, "Concept-To-Product Traceability models")
untraced_models = defined_model_ids - trace_models
abort "untraced product model IDs: #{untraced_models.to_a.sort.join(', ')}" unless untraced_models.empty?

abort "Product Brief must cite rather than redefine Concept Definitions" if product.include?("## Concept Definitions")
abort "Feature Spec must cite rather than redefine Concept Definitions" if spec.include?("## Concept Definitions")
abort "Product Brief must not own Requirement Product Model" if product.include?("## Requirement Product Model\n")
abort "Feature Spec must not own Requirement Product Model" if spec.include?("## Requirement Product Model\n")

product_refs = table(product, "Accepted Concept References")
product_concepts = product_refs.flat_map { |row| ids(row.fetch("Concept ID", ""), /\bC-[A-Z0-9-]+\b/).to_a }.to_set
assert_defined!(product_concepts, concept_ids, "Product Brief concept references")
assert_confirmed!(product_concepts, confirmed, "Product Brief concept references")
product_refs.each do |row|
  concept_id = row.fetch("Concept ID", "")
  expected_name = canonical_names.fetch(concept_id, nil)
  abort "Product Brief canonical name mismatch for #{concept_id}" unless expected_name == row.fetch("Canonical Name", "")
end

product_coverage = table(product, "Requirement Product Model Coverage")
product_coverage_ids = product_coverage.flat_map do |row|
  ids(row.fetch("Requirement Model ID", ""), /\b(?:REL|PERM|CMD|EVT|FLOW|STATE|PM|EX)-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(product_coverage_ids, defined_model_ids, "Product Brief model coverage")
assert_defined!(product_coverage_ids, trace_models, "Product Brief traced model coverage")

spec_refs = table(spec, "Accepted Concept References")
spec_concepts = spec_refs.flat_map { |row| ids(row.fetch("Concept ID", ""), /\bC-[A-Z0-9-]+\b/).to_a }.to_set
assert_defined!(spec_concepts, concept_ids, "Feature Spec concept references")
assert_confirmed!(spec_concepts, confirmed, "Feature Spec concept references")
spec_refs.each do |row|
  concept_id = row.fetch("Concept ID", "")
  expected_name = canonical_names.fetch(concept_id, nil)
  abort "Feature Spec canonical name mismatch for #{concept_id}" unless expected_name == row.fetch("Canonical Name", "")
end

spec_trace = table(spec, "Requirement Product Model Trace")
spec_model_ids = spec_trace.flat_map do |row|
  ids(row.fetch("Requirement Model ID", ""), /\b(?:REL|PERM|CMD|EVT|FLOW|STATE|PM|EX)-[A-Z0-9-]+\b/).to_a +
    ids(row.fetch("Concept / Action / Flow / State IDs", ""), /\b(?:REL|PERM|CMD|EVT|FLOW|STATE|PM|EX)-[A-Z0-9-]+\b/).to_a
end.to_set
spec_trace_concepts = spec_trace.flat_map do |row|
  ids(row.fetch("Concept / Action / Flow / State IDs", ""), /\bC-[A-Z0-9-]+\b/).to_a
end.to_set
assert_defined!(spec_model_ids, defined_model_ids, "Feature Spec model trace")
assert_defined!(spec_model_ids, trace_models, "Feature Spec traced model coverage")
assert_defined!(spec_trace_concepts, concept_ids, "Feature Spec concept trace")
assert_confirmed!(spec_trace_concepts, confirmed, "Feature Spec concept trace")

puts "PASS: accepted Concept Foundation trace is complete (#{concept_ids.length} concepts, #{defined_model_ids.length} model rows)"
