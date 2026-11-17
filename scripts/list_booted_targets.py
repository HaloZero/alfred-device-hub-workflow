#!/usr/bin/env python3
"""Script Filter step one for `simapp`/`simlink`: pick which booted simulator(s) to target."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import common


def main():
    booted = common.list_booted_devices()
    if not booted:
        common.alfred_items([common.info_item(
            "No simulators are currently booted",
            "Run simopen first to boot a simulator.",
        )])
        return

    items = []
    if len(booted) > 1:
        items.append({
            "title": "All Booted Simulators",
            "subtitle": f"Target all {len(booted)} currently running simulators",
            "arg": "All Booted Simulators",
            "variables": {"target": "ALL", "target_label": "All Booted Simulators"},
        })

    for d in booted:
        items.append({
            "title": d["name"],
            "subtitle": f"🟢 Booted · {d['runtime_name']}",
            "arg": d["name"],
            "variables": {"target": d["udid"], "target_label": d["name"]},
        })

    common.alfred_items(items)


if __name__ == "__main__":
    main()
