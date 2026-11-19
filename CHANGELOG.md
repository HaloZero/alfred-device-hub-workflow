# Changelog

All notable changes to this workflow are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Changed

- `simopen`/`simnew` now target **Device Hub** (`com.apple.dt.Devices`,
  bundled at `Xcode.app/Contents/Applications/DeviceHub.app`), Xcode 26's
  replacement for the standalone Simulator.app. They open the picked
  simulator with `open "devices://device/open?id=<udid>"` instead of
  `open -n -a Simulator --args -CurrentDeviceUDID`. Unlike Simulator.app,
  Device Hub's URL scheme focuses the requested device even when it's
  already running, so the `-n`/new-instance workaround from 1.0.4 is no
  longer needed. Requires Xcode 26+; there's no fallback to Simulator.app
  for older Xcode installs.

## [1.0.4] - 2026-11-18

### Fixed

- `simopen`/`simnew` now launch Simulator with `open -n` so a new instance is
  always started. Without `-n`, `--args -CurrentDeviceUDID` was silently
  dropped whenever Simulator.app was already running, so picking a different
  (already-booted) simulator did nothing visible — it just refocused whatever
  window was already in front instead of showing the picked device's own
  window.

## [1.0.3] - 2026-11-18

### Added

- New workflow icon (iPhone + iPad side by side), replacing the placeholder
  added at 1.0.0.
- Friendly handling when the Xcode Command Line Tools aren't installed or
  configured: every Script Filter and Run Script action now checks
  `xcrun --find simctl` up front and fails with a clear Alfred message
  instead of a Python traceback or a cryptic shell error. (`/usr/bin/xcrun`
  ships with macOS itself and is always on PATH, even with no Xcode
  installed, so checking PATH alone wasn't enough — this probes that
  `simctl` actually resolves.)
- `simopen`/`simnew` pass `-CurrentDeviceUDID` so Simulator shows the
  specific picked device rather than whatever window happened to be in
  front. (First pass — only fully fixed once Simulator is already running
  in 1.0.4.)

### Changed

- README rewritten to follow Alfred's Gallery README style guide: `## Usage`
  phrased as "Search ... via the `X` keyword", a `## Setup` section moved
  above `## Usage`, and the configuration section renamed to "Workflow
  Configuration".

## [1.0.0] - 2026-11-16

### Added

- Initial release: `simnew`, `simopen`, `simapp`, `simlink` keywords for
  creating/booting simulators, launching installed apps, and firing deep
  links at currently booted simulator(s).
- Apps shortlist and deep links configured through Alfred's built-in
  Workflow Configuration sheet (`apps_config`, `deeplinks_config`) instead of
  a custom update/config script.
- Self-update via Alfred's built-in GitHub-releases updater.
- Workflow icon.
