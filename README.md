# alfred-device-hub-workflow

Control iOS Simulators from Alfred — create, open, install/launch apps, and fire
deep links at whichever simulators are currently booted. 

## Keywords

| Keyword     | Does |
|-------------|------|
| `simnew`    | Pick a device type + iOS version, creates and boots a new simulator |
| `simopen`   | Pick any existing simulator, boots it (if needed) and brings it to front |
| `simapp`    | Pick currently booted simulator(s) (or "All Booted"), then an installed app (optionally shortlisted via `apps_config`), and launches it |
| `simlink`   | Pick currently booted simulator(s), then a deep link from the `deeplinks_config` workflow variable — or just type a full `scheme://...` URL — and opens it |

`simapp` and `simlink` only ever target simulators that are already booted —
use `simopen` (or `simnew`) first to get one running.

## Configuring your apps and deep links

Open this workflow in Alfred's workflow editor, click the `[x]` (Workflow
Variables) icon in the top toolbar, and edit two variables there — no files
to touch, and the values survive workflow updates:

- `apps_config` — optional JSON array of app names to shortlist, e.g.
  `["Whatnot","Settings"]`. Bundle IDs are looked up automatically from
  whatever's actually installed on the simulator (`simctl listapps`) — you
  never need to know or paste one. Leave it as `[]` to see every installed
  app instead of a shortlist.
- `deeplinks_config` — JSON array of `{ "name", "url" }`. Example:
  ```json
  [{"name":"Home","url":"whatnot://home"}]
  ```

## Installing

1. Open this repo's `info.plist` with Alfred (double-click it, or `open info.plist`),
   or clone the whole repo and symlink/copy it into
   `~/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows/`.
2. In Alfred's workflow editor, confirm each Script Filter/Run Script object's
   working directory resolves to this repo — Alfred runs scripts with the
   workflow folder as the cwd, so this should just work out of the box.

## Releasing an update

Alfred has a built-in updater for workflows whose `info.plist` has a
`webaddress` pointing at a GitHub repo (already set to this repo) and a
`version` string. Alfred periodically checks that repo's releases itself —
no custom command needed. When a newer release exists, Alfred shows an
"Update Available" prompt for this workflow in Alfred Preferences →
Workflows, and the user updates with one click there.

To cut a release:

```bash
# 1. Bump the version in info.plist (the <key>version</key> string), commit it.
# 2. Build the .alfredworkflow package:
scripts/build.sh            # -> dist/Device-Hub-<version>.alfredworkflow

# 3. Tag and create a GitHub release with that file attached:
git tag v1.1.0
git push origin v1.1.0
gh release create v1.1.0 dist/Device-Hub-1.1.0.alfredworkflow --title v1.1.0 --notes "..."
```

Workflow variables (`apps_config`, `deeplinks_config`) are preserved across
updates — only the blueprint (keywords/scripts) gets replaced.

## Scripts

All logic lives in plain Python 3 (`scripts/*.py`, driven by `xcrun simctl`)
and small Bash action scripts (`scripts/*.sh`). Nothing beyond Xcode's
command line tools and Python 3 (both ship with a normal Xcode install) is
required.
