#!/usr/bin/env python3
"""Script Filter step two for `simapp`: pick which configured app to install/launch."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import common

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "apps.json")


def main():
    try:
        with open(CONFIG_PATH) as f:
            apps = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        common.alfred_items([common.info_item(
            "Couldn't read config/apps.json",
            str(exc),
        )])
        return

    if not apps:
        common.alfred_items([common.info_item(
            "No apps configured",
            "Add entries to config/apps.json: name, bundle_id, path (optional).",
        )])
        return

    target_label = os.environ.get("target_label", "selected simulator(s)")

    items = []
    for app in apps:
        path = app.get("path") or ""
        install_note = "Install + Launch" if path else "Launch (already installed)"
        items.append({
            "title": app["name"],
            "subtitle": f"{install_note} on {target_label} · {app['bundle_id']}",
            "arg": app["name"],
            "variables": {
                "bundle_id": app["bundle_id"],
                "app_path": path,
                "app_name": app["name"],
            },
        })

    common.alfred_items(items)


if __name__ == "__main__":
    main()
