"""Shared helpers for Device Hub's Alfred script filters/actions."""
import json
import subprocess
import sys


def simctl(*args):
    result = subprocess.run(
        ["xcrun", "simctl", *args],
        capture_output=True,
        text=True,
    )
    return result


def simctl_json(*args):
    result = simctl(*args, "-j")
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def runtime_display_name(runtime_id):
    """com.apple.CoreSimulator.SimRuntime.iOS-18-6 -> iOS 18.6"""
    short = runtime_id.rsplit(".SimRuntime.", 1)[-1]
    platform, _, version = short.partition("-")
    return f"{platform} {version.replace('-', '.')}" if version else short


def list_devices():
    """Return [{udid, name, state, runtime_id, runtime_name}] for available devices."""
    data = simctl_json("list", "devices", "available")
    if not data:
        return []
    devices = []
    for runtime_id, entries in data.get("devices", {}).items():
        runtime_name = runtime_display_name(runtime_id)
        for entry in entries:
            devices.append({
                "udid": entry["udid"],
                "name": entry["name"],
                "state": entry["state"],
                "runtime_id": runtime_id,
                "runtime_name": runtime_name,
            })
    return devices


def list_booted_devices():
    return [d for d in list_devices() if d["state"] == "Booted"]


def list_installed_apps(udid):
    """Return [{name, bundle_id}] installed on the given simulator.

    `simctl listapps` only emits the legacy OpenStep plist format (its -j
    flag is ignored), so pipe through `plutil` to get JSON.
    """
    listapps = subprocess.run(
        ["xcrun", "simctl", "listapps", udid],
        capture_output=True, text=True,
    )
    if listapps.returncode != 0:
        return []
    convert = subprocess.run(
        ["plutil", "-convert", "json", "-o", "-", "-"],
        input=listapps.stdout, capture_output=True, text=True,
    )
    if convert.returncode != 0:
        return []
    try:
        data = json.loads(convert.stdout)
    except json.JSONDecodeError:
        return []

    apps = [
        {
            "name": info.get("CFBundleDisplayName") or info.get("CFBundleName") or bundle_id,
            "bundle_id": bundle_id,
        }
        for bundle_id, info in data.items()
    ]
    apps.sort(key=lambda a: a["name"].lower())
    return apps


def alfred_items(items):
    sys.stdout.write(json.dumps({"items": items}))


def info_item(title, subtitle=""):
    return {
        "title": title,
        "subtitle": subtitle,
        "valid": False,
    }
