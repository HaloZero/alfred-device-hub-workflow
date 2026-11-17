#!/usr/bin/env python3
"""Script Filter step two for `simlink`: pick a configured deep link, or type a custom URL."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import common


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    target_label = os.environ.get("target_label", "selected simulator(s)")

    items = []

    if "://" in query:
        items.append({
            "title": f"Open custom URL: {query}",
            "subtitle": f"Enter to open on {target_label}",
            "arg": query,
            "variables": {"deeplink_url": query, "deeplink_name": "Custom URL"},
        })

    try:
        links = json.loads(os.environ.get("deeplinks_config") or "[]")
    except json.JSONDecodeError as exc:
        links = []
        if not items:
            common.alfred_items([common.info_item("deeplinks_config variable isn't valid JSON", str(exc))])
            return

    for link in links:
        if query and query.lower() not in link["name"].lower() and "://" not in query:
            continue
        items.append({
            "title": link["name"],
            "subtitle": f"{link['url']} → {target_label}",
            "arg": link["name"],
            "variables": {"deeplink_url": link["url"], "deeplink_name": link["name"]},
        })

    if not items:
        items = [common.info_item(
            "No matching deep link",
            "Type a full URL (scheme://...) to open it directly, or add one to the deeplinks_config workflow variable",
        )]

    common.alfred_items(items)


if __name__ == "__main__":
    main()
