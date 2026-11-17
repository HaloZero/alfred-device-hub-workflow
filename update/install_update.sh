#!/bin/bash
# Run Script action for `simupdate`. Downloads the new .alfredworkflow release
# asset and opens it, which hands off to Alfred's own install/update UI.
set -euo pipefail

: "${download_url:?download_url not set}"

tmp=$(mktemp -d)
dest="$tmp/device-hub-update.alfredworkflow"

curl -fL --retry 2 -o "$dest" "$download_url"
open "$dest"

osascript -e "display notification \"${latest_version:-new version} downloaded — follow Alfred's install prompt\" with title \"Device Hub Update\""
