#!/bin/bash
# Run Script action for `simnew`. Reads device_type_id/device_type_name/runtime_id
# from workflow variables set by scripts/list_device_types.py.
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"
require_xcrun

: "${device_type_id:?device_type_id not set}"
: "${runtime_id:?runtime_id not set}"

name="${device_type_name:-Device Hub Sim} $(date +%H%M%S)"

udid=$(xcrun simctl create "$name" "$device_type_id" "$runtime_id")

xcrun simctl boot "$udid"
open "devices://device/open?id=$udid"

osascript -e "display notification \"${device_type_name:-Simulator} (${runtime_name:-})\" with title \"Simulator Created\""
