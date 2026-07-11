#!/usr/bin/env bash
set -euo pipefail

ruby - "$@" <<'RUBY'
template = nil
target = nil
check_sources = true

args = ARGV.dup
until args.empty?
  arg = args.shift
  case arg
  when "--template"
    template = args.shift
  when "--target"
    target = args.shift
  when "--no-source-check"
    check_sources = false
  when "-h", "--help"
    puts <<~HELP
      Usage: check-root-agents-blocks.sh --template <root-AGENTS.md> --target <AGENTS.md> [--no-source-check]

      Read-only checker for agent-loop root AGENTS managed blocks.
      It verifies marker structure, required section presence, and per-section block-version.
    HELP
    exit 0
  else
    warn "Unknown argument: #{arg}"
    exit 2
  end
end

unless template && target
  warn "Usage: check-root-agents-blocks.sh --template <root-AGENTS.md> --target <AGENTS.md> [--no-source-check]"
  exit 2
end

unless File.file?(template)
  warn "Template not found: #{template}"
  exit 2
end

unless File.file?(target)
  warn "Target not found: #{target}"
  exit 2
end

START_RE = /<!--\s*agent-loop:managed-start\s+([^>]*)-->/
END_RE = /<!--\s*agent-loop:managed-end\s+section:([^\s>]+)\s*-->/

def attr_value(attrs, name)
  match = attrs.match(/(?:^|\s)#{Regexp.escape(name)}:([^\s>]+)/)
  match && match[1]
end

def parse_blocks(path)
  blocks = {}
  errors = []
  active = nil

  File.readlines(path, chomp: true).each_with_index do |line, idx|
    line_no = idx + 1

    if line.scan(/agent-loop:managed-(?:start|end)/).length > 1
      errors << { section: "(unknown)", status: "malformed-marker", detail: "multiple managed markers on one line at line #{line_no}" }
      next
    end

    if (match = line.match(START_RE))
      attrs = match[1]
      section = attr_value(attrs, "section")
      unless section
        errors << { section: "(unknown)", status: "malformed-marker", detail: "start marker at line #{line_no} is missing section" }
        next
      end

      if active
        errors << { section: active[:section], status: "broken-markers", detail: "section #{active[:section]} starts at line #{active[:start_line]} but is not closed before line #{line_no}" }
        errors << { section: active[:section], status: "nested-managed-block", detail: "section #{active[:section]} starts at line #{active[:start_line]} but a nested section starts at line #{line_no}" }
      end

      if blocks.key?(section)
        errors << { section: section, status: "duplicate-section", detail: "section #{section} appears more than once" }
      end

      active = {
        section: section,
        attrs: attrs,
        source: attr_value(attrs, "source"),
        version: attr_value(attrs, "version"),
        block_version: attr_value(attrs, "block-version"),
        start_line: line_no
      }
      next
    end

    if line.include?("agent-loop:managed-start")
      errors << { section: "(unknown)", status: "malformed-marker", detail: "malformed managed-start marker at line #{line_no}" }
      next
    end

    if (match = line.match(END_RE))
      end_section = match[1]
      unless active
        errors << { section: end_section, status: "broken-markers", detail: "orphan end marker at line #{line_no}" }
        next
      end

      if active[:section] != end_section
        errors << { section: active[:section], status: "broken-markers", detail: "section #{active[:section]} starts at line #{active[:start_line]} but ends as #{end_section} at line #{line_no}" }
        active = nil
        next
      end

      blocks[active[:section]] = active.merge(end_line: line_no)
      active = nil
      next
    end

    if line.include?("agent-loop:managed-end")
      errors << { section: "(unknown)", status: "malformed-marker", detail: "malformed managed-end marker at line #{line_no}" }
      next
    end
  end

  if active
    errors << { section: active[:section], status: "broken-markers", detail: "section #{active[:section]} starts at line #{active[:start_line]} but has no end marker" }
  end

  [blocks, errors]
end

def local_source?(source)
  return false unless source
  return false if source == "agent-loop-skill"
  return false if source.start_with?("http://", "https://")
  source.include?("/") || source.end_with?(".md")
end

template_blocks, template_errors = parse_blocks(template)
target_blocks, target_errors = parse_blocks(target)

findings = []

template_errors.each do |err|
  findings << [err[:section], err[:status], "-", "-", err[:detail], "fix template markers"]
end

target_errors.each do |err|
  tmpl = template_blocks[err[:section]]
  findings << [
    err[:section],
    err[:status],
    tmpl ? tmpl[:block_version].to_s : "-",
    "-",
    err[:detail],
    "repair target managed markers before refresh"
  ]
end

template_blocks.each do |section, tmpl|
  target_block = target_blocks[section]

  unless target_block
    findings << [
      section,
      "missing",
      tmpl[:block_version].to_s,
      "none",
      "template section is absent from target AGENTS.md",
      "add managed block after human review"
    ]
    next
  end

  if target_block[:block_version].nil? || target_block[:block_version].empty?
    findings << [
      section,
      "missing-block-version",
      tmpl[:block_version].to_s,
      "none",
      "expected #{tmpl[:block_version]}",
      "refresh marker metadata after human review"
    ]
  elsif target_block[:block_version] != tmpl[:block_version]
    findings << [
      section,
      "stale-block-version",
      tmpl[:block_version].to_s,
      target_block[:block_version].to_s,
      "expected #{tmpl[:block_version]}, found #{target_block[:block_version]}",
      "refresh managed block after human review"
    ]
  end

  next unless check_sources && local_source?(target_block[:source])

  source_path = File.expand_path(target_block[:source], File.dirname(target))
  unless File.exist?(source_path)
    findings << [
      section,
      "source-missing",
      tmpl[:block_version].to_s,
      target_block[:block_version].to_s,
      "source #{target_block[:source]} does not exist relative to #{File.dirname(target)}",
      "verify source path or update block source after human review"
    ]
  end
end

target_blocks.each do |section, target_block|
  next if template_blocks.key?(section)
  findings << [
    section,
    "unexpected-managed-section",
    "none",
    target_block[:block_version].to_s,
    "target section is not present in template",
    "ask whether to keep, migrate, or remove"
  ]
end

if findings.empty?
  puts "PASS root AGENTS managed blocks are current"
  exit 0
end

puts "FAIL root AGENTS drift found"
puts
puts "| Section | Status | Template Block | Target Block | Detail | Action |"
puts "|---|---|---|---|---|---|"
findings.each do |row|
  puts "| #{row.map { |cell| cell.to_s.gsub("|", "\\|") }.join(" | ")} |"
end
exit 1
RUBY
