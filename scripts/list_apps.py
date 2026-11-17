#!/usr/bin/env python3
"""Script Filter step two for `simapp`: pick which configured app to install/launch."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import common


def main():
    try:
        apps = json.loads(os.environ.get("apps_config") or "[]")
    except json.JSONDecodeError as exc:
        common.alfred_items([common.info_item(
            "apps_config variable isn't valid JSON",
            str(exc),
        )])
        return

    if not apps:
        common.alfred_items([common.info_item(
            "No apps configured",
            "Set the apps_config workflow variable: [{name, bundle_id, path}, ...]",
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
