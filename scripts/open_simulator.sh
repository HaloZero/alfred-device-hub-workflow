#!/bin/bash
# Run Script action for `simopen`. Boots (if needed) and focuses the chosen simulator.
set -uo pipefail

: "${udid:?udid not set}"

xcrun simctl boot "$udid" 2>/dev/null
open -a Simulator

osascript -e "display notification \"${device_name:-Simulator}\" with title \"Simulator Opened\""
