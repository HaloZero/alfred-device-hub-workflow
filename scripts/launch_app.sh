#!/bin/bash
# Run Script action for `simapp`. Installs (if a path was configured) and launches
# the chosen app on the chosen target(s): a single udid, or "ALL" booted simulators.
set -uo pipefail

: "${target:?target not set}"
: "${bundle_id:?bundle_id not set}"

if [[ "$target" == "ALL" ]]; then
  targets=$(xcrun simctl list devices booted -j | /usr/bin/python3 -c '
import json, sys
data = json.load(sys.stdin)
for entries in data["devices"].values():
    for d in entries:
        print(d["udid"])
')
else
  targets="$target"
fi

if [[ -z "$targets" ]]; then
  osascript -e 'display notification "No booted simulators found" with title "Device Hub"'
  exit 0
fi

while IFS= read -r udid; do
  [[ -z "$udid" ]] && continue
  if [[ -n "${app_path:-}" ]]; then
    xcrun simctl install "$udid" "$app_path"
  fi
  xcrun simctl launch "$udid" "$bundle_id"
done <<< "$targets"

osascript -e "display notification \"${app_name:-App} launched\" with title \"Device Hub\""
