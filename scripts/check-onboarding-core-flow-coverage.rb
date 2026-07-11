#!/usr/bin/env ruby
# frozen_string_literal: true

require "pathname"

class CoverageError < StandardError; end

class CoreFlowCoverage
  FLOW_ID = /CF-[A-Z0-9-]+/
  SLICE_ID = /CF-[A-Z0-9-]+\/S\d{2}/

  def initialize(root)
    @root = Pathname(root).expand_path
  end

  def validate!
    raise CoverageError, "onboarding root not found: #{@root}" unless @root.directory?

    evidence = read_required("08-review/evidence-graph.md", "evidence-graph.md")
    spec = read_required("onboarding-spec.md")
    tasks = read_required("onboarding-tasks.md")
    coverage = read_required("coverage-matrix.md")
    review = read_required("batch-review.md")
    core_flow_rows = evidence.lines.select do |line|
      line.start_with?("|") && line.match?(FLOW_ID) && line.match?(/\|\s*(critical|important)\s*\|/)
    end
    raise CoverageError, "no critical/important core flow rows found" if core_flow_rows.empty?

    planned_count = 0
    deferred_count = 0

    core_flow_rows.each do |row|
      flow_id = row[FLOW_ID]

      require_token(spec, flow_id, "onboarding-spec.md")
      require_token(tasks, flow_id, "onboarding-tasks.md")
      require_token(coverage, flow_id, "coverage-matrix.md")
      require_token(review, flow_id, "batch-review.md")

      if row.match?(/\|\s*deferred\s*\|/)
        validate_deferred!(row, flow_id)
        deferred_count += 1
        next
      end

      unless row.match?(/\|\s*planned\s*\|/)
        raise CoverageError, "core flow selection must be planned or deferred: #{flow_id}"
      end

      planned_count += 1
      validate_planned!(flow_id, spec, tasks, coverage, review)
    end

    puts "PASS: core-flow coverage trace is complete (#{planned_count} planned, #{deferred_count} deferred)"
  end

  private

  def validate_deferred!(row, flow_id)
    %w[impact missing next].each do |field|
      raise CoverageError, "deferred flow missing #{field}: #{flow_id}" unless row.match?(/\b#{field}\s*=/i)
    end
  end

  def validate_planned!(flow_id, spec, tasks, coverage, review)
    required_slices = spec.scan(/#{Regexp.escape(flow_id)}\/S\d{2}/).uniq.sort
    raise CoverageError, "no required slices declared: #{flow_id}" if required_slices.empty?

    required_slices.each { |slice| require_token(tasks, slice, "onboarding-tasks.md") }

    flow_text = read_flow_docs.select { |text| text.include?(flow_id) }.join("\n")
    raise CoverageError, "missing flow document: #{flow_id}" if flow_text.empty?

    forbidden = flow_text.match(/<\.\.\.|TBD|TODO|待补充|看代码|see code/i)
    raise CoverageError, "unresolved placeholder in flow document: #{flow_id}" if forbidden

    slice_rows = required_slices.map do |slice|
      row = flow_text.lines.find { |line| line.start_with?("|") && line.include?(slice) }
      raise CoverageError, "missing required slice: #{slice}" unless row
      raise CoverageError, "slice is not covered: #{slice}" unless row.match?(/\|\s*covered\s*\|/)
      raise CoverageError, "slice missing Diagram ID: #{slice}" unless row.match?(/D-[A-Z0-9-]+/)
      raise CoverageError, "slice missing document section: #{slice}" unless row.match?(/§\d+/)
      [slice, row]
    end

    required_diagrams = (spec.scan(/D-[A-Z0-9-]+/) + tasks.scan(/D-[A-Z0-9-]+/) + slice_rows.flat_map { |_slice, row| row.scan(/D-[A-Z0-9-]+/) }).uniq
    required_diagrams.each do |diagram_id|
      defined = flow_text.lines.any? do |line|
        !line.start_with?("|") && line.include?(diagram_id) && (line.start_with?("#") || line.match?(/Diagram ID/i))
      end
      raise CoverageError, "missing diagram definition: #{diagram_id}" unless defined
    end

    slice_rows.each do |slice, row|
      row.scan(/§(\d+)/).flatten.each do |section_number|
        heading_pattern = Regexp.new("^" + "#" + "{2,6}\\s+" + Regexp.escape(section_number) + "(?:\\.|\\s)")
        unless flow_text.match?(heading_pattern)
          raise CoverageError, "missing document section: #{slice} -> §#{section_number}"
        end
      end
      raise CoverageError, "slice missing symbol/config evidence: #{slice}" unless row.match?(/`[^`]+#[^`]+`/)
    end

    unless flow_text.match?(/Call \/ Data Direction|\|\s*Direction\s*\|/i)
      raise CoverageError, "flow missing call/data direction evidence: #{flow_id}"
    end

    require_hard_gate_before_score(coverage, "coverage-matrix.md")
    require_hard_gate_before_score(review, "batch-review.md")
    require_hard_gate_pass(coverage, flow_id, "coverage-matrix.md")
    require_hard_gate_pass(review, flow_id, "batch-review.md")
  end

  def read_required(*candidates)
    path = candidates.map { |candidate| @root.join(candidate) }.find(&:file?)
    raise CoverageError, "missing artifact: #{candidates.first}" unless path

    path.read
  end

  def read_flow_docs
    paths = @root.glob("03-flows/*.md")
    paths = [@root.join("flow.md")] if paths.empty? && @root.join("flow.md").file?
    raise CoverageError, "missing artifact: 03-flows/*.md" if paths.empty?

    paths.map(&:read)
  end

  def require_token(text, token, artifact)
    raise CoverageError, "missing #{token} in #{artifact}" unless text.include?(token)
  end

  def require_hard_gate_pass(text, flow_id, artifact)
    row = text.lines.find { |line| line.start_with?("|") && line.include?(flow_id) && line.match?(/\|\s*PASS\s*\|/) }
    raise CoverageError, "Completeness Hard Gate is not PASS for #{flow_id} in #{artifact}" unless row
  end

  def require_hard_gate_before_score(text, artifact)
    gate_index = text.index("Completeness Hard Gate")
    raise CoverageError, "missing Completeness Hard Gate in #{artifact}" unless gate_index

    score_index = text.index("## Score")
    if score_index && gate_index > score_index
      raise CoverageError, "Completeness Hard Gate must precede score in #{artifact}"
    end
  end
end

if ARGV.length != 1
  warn "usage: ruby scripts/check-onboarding-core-flow-coverage.rb ONBOARDING_ROOT"
  exit 2
end

begin
  CoreFlowCoverage.new(ARGV.fetch(0)).validate!
rescue CoverageError => e
  warn e.message
  exit 1
end
