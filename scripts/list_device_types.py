#!/usr/bin/env python3
"""Script Filter for `simnew`: list device type x runtime combos that can be created."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import common


def main():
    device_types = common.simctl_json("list", "devicetypes")
    runtimes = common.simctl_json("list", "runtimes")
    if not device_types or not runtimes:
        common.alfred_items([common.info_item(
            "Could not read Xcode Simulator data",
            "Make sure Xcode and its Command Line Tools are installed.",
        )])
        return

    available_runtimes = [r for r in runtimes["runtimes"] if r.get("isAvailable")]
    # Newest runtimes first so recent iOS versions surface at the top.
    available_runtimes.sort(key=lambda r: r.get("version", ""), reverse=True)

    items = []
    for runtime in available_runtimes:
        supported = {d["identifier"] for d in runtime.get("supportedDeviceTypes", [])}
        for device_type in device_types["devicetypes"]:
            if device_type["identifier"] not in supported:
                continue
            items.append({
                "title": f"{device_type['name']} — {runtime['name']}",
                "subtitle": "Enter to create this simulator",
                "arg": f"{device_type['name']} {runtime['name']}",
                "variables": {
                    "device_type_id": device_type["identifier"],
                    "device_type_name": device_type["name"],
                    "runtime_id": runtime["identifier"],
                    "runtime_name": runtime["name"],
                },
            })

    if not items:
        items = [common.info_item("No available runtimes found",
                                   "Install a Simulator runtime in Xcode > Settings > Platforms")]

    common.alfred_items(items)


if __name__ == "__main__":
    main()
