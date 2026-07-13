#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "open3"
require "tmpdir"

root = File.expand_path("..", __dir__)
validator = File.join(root, "scripts/check-concept-foundation-trace.rb")
example_dir = File.join(root, "examples/concept-foundation-refund")

base_requirement = File.read(File.join(example_dir, "requirement.md"))
base_product = File.read(File.join(example_dir, "product.md"))
base_spec = File.read(File.join(example_dir, "spec.md"))

def expect_reject(name, validator, requirement, product, spec)
  Dir.mktmpdir("concept-foundation-adversarial") do |dir|
    requirement_path = File.join(dir, "requirement.md")
    product_path = File.join(dir, "product.md")
    spec_path = File.join(dir, "spec.md")

    File.write(requirement_path, requirement)
    File.write(product_path, product)
    File.write(spec_path, spec)

    _stdout, _stderr, status = Open3.capture3(
      "ruby",
      validator,
      requirement_path,
      product_path,
      spec_path
    )

    abort "FAIL: validator accepted adversarial case: #{name}" if status.success?
  end

  puts "PASS: validator rejected #{name}"
end

expect_reject(
  "downstream use of unconfirmed concepts",
  validator,
  base_requirement.sub(
    /^- Confirmed Concept IDs:.*/,
    "- Confirmed Concept IDs: C-CUSTOMER"
  ),
  base_product,
  base_spec
)

expect_reject(
  "missing Concept Candidate Inventory",
  validator,
  base_requirement.sub(
    /^## Concept Candidate Inventory\n.*?(?=^## Concept Definitions\n)/m,
    ""
  ),
  base_product,
  base_spec
)

expect_reject(
  "open blocking ambiguity",
  validator,
  base_requirement.sub("| resolved |", "| open |"),
  base_product,
  base_spec
)

not_needed_requirement = base_requirement
  .sub("Concept Foundation Status: accepted", "Concept Foundation Status: concept-foundation-not-needed")
  .sub(/^Not-Needed Reason:.*/, "Not-Needed Reason: n/a")
not_needed_product = base_product.sub(
  "Concept Foundation Status: accepted",
  "Concept Foundation Status: concept-foundation-not-needed"
)
not_needed_spec = base_spec.sub(
  "Concept Foundation Status: accepted",
  "Concept Foundation Status: concept-foundation-not-needed"
)

expect_reject(
  "non-concrete concept-foundation-not-needed reason",
  validator,
  not_needed_requirement,
  not_needed_product,
  not_needed_spec
)

expect_reject(
  "downstream model omitted from Concept-To-Product trace",
  validator,
  base_requirement.sub(/^\| TRACE-03 .*\n/, ""),
  base_product,
  base_spec
)

duplicate_definition = File.readlines(File.join(example_dir, "requirement.md"))
  .find { |line| line.start_with?("| C-CUSTOMER |") }
duplicate_requirement = base_requirement.sub(
  duplicate_definition,
  duplicate_definition * 2
)

expect_reject(
  "duplicate Concept Definition ID",
  validator,
  duplicate_requirement,
  base_product,
  base_spec
)

expect_reject(
  "missing effective Concept Foundation source",
  validator,
  base_requirement,
  base_product.sub(/^Effective Concept Source:.*\n/, ""),
  base_spec
)

expect_reject(
  "command actor without target permission",
  validator,
  base_requirement.sub(/^\| C-REFUND-ADMIN \| C-REFUND-SETTLEMENT .*\n/, ""),
  base_product,
  base_spec
)

puts "PASS: Concept Foundation adversarial trace cases are rejected"
