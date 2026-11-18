#!/bin/bash
# Run Script action for `simopen`. Boots (if needed) and focuses the chosen simulator.
set -uo pipefail

source "$(dirname "$0")/lib/common.sh"
require_xcrun

: "${udid:?udid not set}"

xcrun simctl boot "$udid" 2>/dev/null
open -a Simulator --args -CurrentDeviceUDID "$udid"

osascript -e "display notification \"${device_name:-Simulator}\" with title \"Simulator Opened\""
