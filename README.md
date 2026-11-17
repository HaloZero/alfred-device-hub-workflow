# alfred-device-hub-workflow

Control iOS Simulators from Alfred — create, open, install/launch apps, and fire
deep links at whichever simulators are currently booted. Updates itself from
this GitHub repo's releases.

## Keywords

| Keyword     | Does |
|-------------|------|
| `simnew`    | Pick a device type + iOS version, creates and boots a new simulator |
| `simopen`   | Pick any existing simulator, boots it (if needed) and brings it to front |
| `simapp`    | Pick currently booted simulator(s) (or "All Booted"), then an app from `config/apps.json`, installs (if a path is set) and launches it |
| `simlink`   | Pick currently booted simulator(s), then a deep link from `config/deeplinks.json` — or just type a full `scheme://...` URL — and opens it |
| `simupdate` | Checks this repo's latest GitHub release against the installed version and installs it if newer |

`simapp` and `simlink` only ever target simulators that are already booted —
use `simopen` (or `simnew`) first to get one running.

## Configuring your apps and deep links

Edit these two files and keep them in version control alongside the workflow:

- `config/apps.json` — `{ "name", "bundle_id", "path" }`. Leave `path` empty
  (`""`) to just launch an app that's already installed on the simulator;
  set it to a built `.app` bundle path to install it first.
- `config/deeplinks.json` — `{ "name", "url" }`.

## Installing

1. Open this repo's `info.plist` with Alfred (double-click it, or `open info.plist`),
   or clone the whole repo and symlink/copy it into
   `~/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows/`.
2. In Alfred's workflow editor, confirm each Script Filter/Run Script object's
   working directory resolves to this repo — Alfred runs scripts with the
   workflow folder as the cwd, so this should just work out of the box.

## Releasing an update

`simupdate` looks at `https://github.com/HaloZero/alfred-device-hub-workflow/releases/latest`
for a release whose tag is newer than the installed `version` (set in `info.plist`)
and that has a `.alfredworkflow` asset attached.

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

Anyone running `simupdate` will then be offered that release and, on Enter,
Alfred downloads and installs it.

## Scripts

All logic lives in plain Python 3 (`scripts/*.py`, driven by `xcrun simctl`)
and small Bash action scripts (`scripts/*.sh`). Nothing beyond Xcode's
command line tools and Python 3 (both ship with a normal Xcode install) is
required.
