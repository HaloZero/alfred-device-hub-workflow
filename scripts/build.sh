#!/bin/bash
# Packages this repo into a .alfredworkflow (a zip) for a GitHub release.
# Usage: scripts/build.sh [version]
#   - Reads the version from info.plist unless one is passed.
#   - Writes dist/Device-Hub-<version>.alfredworkflow
set -euo pipefail
cd "$(dirname "$0")/.."

version="${1:-$(/usr/libexec/PlistBuddy -c 'Print :version' info.plist)}"
out_dir="dist"
out_file="$out_dir/Device-Hub-${version}.alfredworkflow"

mkdir -p "$out_dir"
rm -f "$out_file"

zip -r "$out_file" \
  info.plist \
  scripts \
  -x '*.pyc' -x '__pycache__/*' -x '*/__pycache__/*'

echo "Built $out_file"
