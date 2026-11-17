#!/usr/bin/env python3
"""Script Filter for `simupdate`: check GitHub releases for a newer version."""
import json
import os
import sys
import urllib.request

REPO = "HaloZero/alfred-device-hub-workflow"


def current_version():
    return os.environ.get("alfred_workflow_version", "0.0.0")


def version_tuple(v):
    v = v.lstrip("vV")
    parts = []
    for p in v.split("."):
        digits = "".join(c for c in p if c.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def fetch_latest_release():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.load(resp)


def main():
    current = current_version()
    try:
        release = fetch_latest_release()
    except Exception as exc:
        print(json.dumps({"items": [{
            "title": "Couldn't check for updates",
            "subtitle": str(exc),
            "valid": False,
        }]}))
        return

    latest = release.get("tag_name", "0.0.0")
    asset = next((a for a in release.get("assets", [])
                   if a["name"].endswith(".alfredworkflow")), None)

    if not asset:
        print(json.dumps({"items": [{
            "title": f"Latest release {latest} has no .alfredworkflow asset",
            "subtitle": "Nothing to install.",
            "valid": False,
        }]}))
        return

    if version_tuple(latest) <= version_tuple(current):
        print(json.dumps({"items": [{
            "title": f"Up to date (v{current})",
            "subtitle": f"Latest release is {latest}.",
            "valid": False,
        }]}))
        return

    print(json.dumps({"items": [{
        "title": f"Update available: v{current} → {latest}",
        "subtitle": "Press Enter to download and install.",
        "arg": asset["browser_download_url"],
        "variables": {"download_url": asset["browser_download_url"], "latest_version": latest},
    }]}))


if __name__ == "__main__":
    main()
