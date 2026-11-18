# Shared helpers for Device Hub's Bash Run Script actions.

# Bail out with a clear Alfred notification if the Xcode Command Line Tools
# aren't installed, instead of letting `xcrun`/`simctl` fail cryptically.
#
# `/usr/bin/xcrun` ships with macOS itself and is always on PATH, even with no
# Xcode or Command Line Tools installed — it just errors when invoked. So
# `command -v xcrun` alone isn't enough; `xcrun --find` is a lightweight way
# to probe whether it can actually resolve a real tool.
require_xcrun() {
  if ! command -v xcrun >/dev/null 2>&1 || ! xcrun --find simctl >/dev/null 2>&1; then
    osascript -e 'display notification "Install Xcode (or run xcode-select --install)" with title "Xcode Command Line Tools Not Found"' >/dev/null 2>&1
    echo "xcrun/simctl not available — install Xcode or run \`xcode-select --install\`." >&2
    exit 1
  fi
}
