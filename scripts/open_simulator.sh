#!/bin/bash
# Run Script action for `simopen`. Boots (if needed) and focuses the chosen simulator.
set -uo pipefail

source "$(dirname "$0")/lib/common.sh"
require_xcrun

: "${udid:?udid not set}"

xcrun simctl boot "$udid" 2>/dev/null
# Xcode 26 replaced Simulator.app with Device Hub. Its `devices://` URL
# scheme focuses a specific device by UDID even while Device Hub is already
# running — unlike Simulator.app's `--args`, which a running instance ignored.
open "devices://device/open?id=$udid"

osascript -e "display notification \"${device_name:-Simulator}\" with title \"Device Hub Opened\""
