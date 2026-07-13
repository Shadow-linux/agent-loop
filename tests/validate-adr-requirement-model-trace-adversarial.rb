#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "open3"
require "tmpdir"

root = File.expand_path("..", __dir__)
validator = File.join(root, "scripts/check-adr-requirement-model-trace.rb")
valid_dir = File.join(root, "tests/fixtures/adr-technical-landing/valid")
not_needed_dir = File.join(root, "tests/fixtures/adr-technical-landing/valid-not-needed")

base_readme = File.read(File.join(valid_dir, "README.md"))
base_source = File.read(File.join(valid_dir, "requirement.md"))
base_decision = File.read(File.join(valid_dir, "decision.md"))

failures = []

def run_validator(validator, fixture_dir, readme, source, decision)
  Dir.mktmpdir("adr-technical-landing-adversarial") do |dir|
    FileUtils.cp_r(File.join(fixture_dir, "."), dir)
    readme_path = File.join(dir, "README.md")
    source_path = File.join(dir, "requirement.md")
    decision_path = File.join(dir, "decision.md")
    File.write(readme_path, readme)
    File.write(source_path, source)
    File.write(decision_path, decision)

    stdout, stderr, status = Open3.capture3(
      "ruby",
      validator,
      readme_path,
      source_path,
      decision_path
    )
    [status.success?, (stdout + stderr).strip]
  end
end

def expect_accept(failures, name, validator, fixture_dir, readme, source, decision)
  accepted, output = run_validator(validator, fixture_dir, readme, source, decision)
  if accepted
    puts "PASS: validator accepted #{name}"
  else
    failures << "expected acceptance for #{name}: #{output.lines.first}"
  end
end

def expect_reject(failures, name, validator, fixture_dir, readme, source, decision)
  accepted, output = run_validator(validator, fixture_dir, readme, source, decision)
  if accepted
    failures << "validator accepted adversarial case: #{name}"
  else
    puts "PASS: validator rejected #{name} (#{output.lines.first})"
  end
end

proposed_decision = base_decision
  .sub(/^Status: accepted$/, "Status: proposed")
  .sub(/^## Human Review Evidence\n.*?(?=^## |\z)/m, "")
expect_accept(
  failures,
  "a proposed ADR structural preflight before Human Review",
  validator,
  valid_dir,
  base_readme,
  base_source,
  proposed_decision
)

expect_accept(
  failures,
  "an accepted ADR with recorded Human Review evidence",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision
)

expect_reject(
  failures,
  "an accepted ADR without recorded Human Review evidence",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub(/^## Human Review Evidence\n.*?(?=^## |\z)/m, "")
)

expect_accept(
  failures,
  "an explicitly planned canonical Feature Spec owner path",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.gsub("features/fixture/spec.md", "planned:features/future-fixture/spec.md")
)

delegated_decision = base_decision
  .sub(", FLOW-FIXTURE-01", "")
  .sub(
    "| FLOW-FIXTURE-01 | in-scope | ADR-9000 |",
    "| FLOW-FIXTURE-01 | proposed-decision | decisions/9001-follow-up.md |"
  )
  .sub(/^\| FLOW-FIXTURE-01 \| source flow reference .*\n/, "")
expect_accept(
  failures,
  "a source model explicitly delegated to an existing proposed decision",
  validator,
  valid_dir,
  base_readme,
  base_source,
  delegated_decision
)

expect_reject(
  failures,
  "placeholder not-applicable reason",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub("reason: outside this coherent decision boundary", "reason: n/a")
)

expect_reject(
  failures,
  "a Coverage Hard Gate replaced by one arbitrary checkbox",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub(/## Coverage Hard Gate\n.*?(?=^## |\z)/m, "## Coverage Hard Gate\n\n- [x] arbitrary check\n\n")
)

expect_reject(
  failures,
  "a Coverage Hard Gate with an unsupported extra checkbox",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub(
    "- [x] No unresolved product-semantic blocker remains",
    "- [x] No unresolved product-semantic blocker remains\n- [x] arbitrary extra check"
  )
)

expect_reject(
  failures,
  "unparsed garbage in Accepted Requirement Model IDs",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub(/^Accepted Requirement Model IDs:(.*)$/, 'Accepted Requirement Model IDs:\1, GARBAGE')
)

expect_reject(
  failures,
  "a source model silently omitted from ADR scope",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision
    .sub(/, PM-FIXTURE-FACT/, "")
    .gsub(/^\| PM-FIXTURE-FACT .*\n/, "")
)

expect_reject(
  failures,
  "a covered-by-accepted-decision reference whose ADR does not exist",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub("decisions/8999-shared.md (ADR-8999)", "decisions/does-not-exist.md (ADR-DOES-NOT-EXIST)")
)

expect_reject(
  failures,
  "a feature-local reference whose Feature Spec does not exist",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub("features/fixture/spec.md", "features/missing/spec.md")
)

expect_reject(
  failures,
  "a Design Slice with an invalid coverage status",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub("| planned |", "| banana |")
)

expect_reject(
  failures,
  "a triggered operational concern without its detail section",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.sub(/\n## Triggered Operational Landing\n.*?(?=\n## Design Slice Coverage)/m, "")
)

expect_reject(
  failures,
  "an incomplete operational concern inventory",
  validator,
  valid_dir,
  base_readme,
  base_source,
  base_decision.gsub(/^\| (?:Compatibility|Rollout \/ Cutover|Rollback \/ Reversibility) \|.*\n/, "")
)

not_needed_readme = File.read(File.join(not_needed_dir, "README.md"))
not_needed_source = File.read(File.join(not_needed_dir, "requirement.md"))
not_needed_decision = File.read(File.join(not_needed_dir, "decision.md"))
expect_accept(
  failures,
  "a reasoned concept-foundation-not-needed ADR preflight without a product model",
  validator,
  not_needed_dir,
  not_needed_readme,
  not_needed_source,
  not_needed_decision
)

abort failures.map { |failure| "FAIL: #{failure}" }.join("\n") unless failures.empty?

puts "PASS: ADR technical landing adversarial contract is complete"
