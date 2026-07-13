#!/usr/bin/env ruby
# frozen_string_literal: true
# DEPRECATED COMPATIBILITY ENTRY: use check-onboarding-core-flow-coverage.py directly.

script = File.expand_path("check-onboarding-core-flow-coverage.py", __dir__)
candidates = ENV["PYTHON"] ? [[ENV["PYTHON"]]] : [["py", "-3"], ["python3"], ["python"]]
python = candidates.find do |candidate|
  system(*candidate, "--version", out: File::NULL, err: File::NULL)
end

unless python
  warn "usage error: Python 3.10+ is required"
  exit 2
end

exec(*python, script, *ARGV)
