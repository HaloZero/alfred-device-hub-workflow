# alfred-device-hub-workflow

Alfred workflow (`info.plist` + `scripts/`) for controlling iOS Simulators:
`simnew`, `simopen`, `simapp`, `simlink`.

## Changelog discipline

- Every notable change (bug fix, behavior change, new capability) gets a
  bullet in `CHANGELOG.md` under `## [Unreleased]` as part of the same piece
  of work — not reconstructed from memory later.
- Use [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) section
  headers under `[Unreleased]` as needed: `### Added`, `### Changed`,
  `### Fixed`, `### Removed`.
- Only when actually cutting a release: rename `[Unreleased]` to
  `[<version>] - <date>`, bump `<key>version</key>` in `info.plist` to match,
  and add a fresh empty `## [Unreleased]` above it.
