#!/usr/bin/env python3
"""Script Filter for `simopen`: list every available simulator, booted or not."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import common


def main():
    if not common.ensure_xcrun():
        return
    devices = common.list_devices()
    if not devices:
        common.alfred_items([common.info_item("No simulators found",
                                                "Use simnew to create one first.")])
        return

    devices.sort(key=lambda d: (d["state"] != "Booted", d["name"]))

    items = []
    for d in devices:
        marker = "🟢 Booted" if d["state"] == "Booted" else "Shutdown"
        items.append({
            "title": d["name"],
            "subtitle": f"{marker} · {d['runtime_name']}",
            "arg": d["name"],
            "variables": {"udid": d["udid"], "device_name": d["name"]},
        })

    common.alfred_items(items)


if __name__ == "__main__":
    main()
