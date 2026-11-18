#!/usr/bin/env python3
"""Script Filter step two for `simapp`: pick which installed app to launch.

Bundle IDs are resolved live from the simulator (`simctl listapps`) — no
need to configure or paste them anywhere. `apps_config` (a JSON array of
names, e.g. ["Whatnot","Settings"]) is just an optional shortlist; leave it
as `[]` to see every installed app instead.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import common


def resolve_query_udid(target):
    if target != "ALL":
        return target
    booted = common.list_booted_devices()
    return booted[0]["udid"] if booted else None


def main():
    if not common.ensure_xcrun():
        return
    target = os.environ.get("target", "")
    target_label = os.environ.get("target_label", "selected simulator(s)")

    udid = resolve_query_udid(target)
    if not udid:
        common.alfred_items([common.info_item(
            "No booted simulators found",
            "Run simopen first to boot a simulator.",
        )])
        return

    apps = common.list_installed_apps(udid)
    if not apps:
        common.alfred_items([common.info_item(
            "Couldn't list installed apps",
            f"`xcrun simctl listapps {udid}` returned nothing.",
        )])
        return

    try:
        shortlist = [n.lower() for n in json.loads(os.environ.get("apps_config") or "[]")]
    except json.JSONDecodeError:
        shortlist = []

    if shortlist:
        apps = [a for a in apps if any(n in a["name"].lower() for n in shortlist)]

    if not apps:
        common.alfred_items([common.info_item(
            "No installed apps match apps_config",
            "Clear the apps_config workflow variable to see every installed app.",
        )])
        return

    items = [{
        "title": app["name"],
        "subtitle": f"Launch on {target_label} · {app['bundle_id']}",
        "arg": app["name"],
        "variables": {"bundle_id": app["bundle_id"], "app_name": app["name"]},
    } for app in apps]

    common.alfred_items(items)


if __name__ == "__main__":
    main()
