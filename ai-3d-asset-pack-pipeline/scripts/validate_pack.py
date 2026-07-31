#!/usr/bin/env python3
"""Validate the release invariants of a manifest-driven asset pack."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FILES = ("manifest.json", "installation.md", "usage.md", "license.md")
VALID_STATUSES = {"draft", "needs_revision", "approved", "rejected"}


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")

    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        return errors
    try:
        manifest = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as exc:
        return errors + [f"invalid manifest JSON: {exc}"]

    for key in ("pack_id", "pack_name", "version", "status", "assets", "provenance"):
        if key not in manifest:
            errors.append(f"manifest missing key: {key}")
    if manifest.get("status") not in VALID_STATUSES:
        errors.append(f"invalid pack status: {manifest.get('status')}")
    if not isinstance(manifest.get("assets"), list):
        errors.append("manifest assets must be a list")
        return errors

    ids: set[str] = set()
    for index, asset in enumerate(manifest["assets"]):
        if not isinstance(asset, dict):
            errors.append(f"asset {index} must be an object")
            continue
        asset_id = asset.get("id")
        if not asset_id:
            errors.append(f"asset {index} missing id")
        elif asset_id in ids:
            errors.append(f"duplicate asset id: {asset_id}")
        else:
            ids.add(asset_id)
        if asset.get("status") not in VALID_STATUSES:
            errors.append(f"asset {asset_id or index} has invalid status")
        for field in ("reference", "model_source", "review"):
            if not asset.get(field):
                errors.append(f"asset {asset_id or index} missing {field}")
        if asset.get("status") == "approved":
            for field in ("preview", "provenance"):
                if not asset.get(field):
                    errors.append(f"approved asset {asset_id} missing {field}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", type=Path)
    args = parser.parse_args()
    errors = validate(args.pack)
    if errors:
        print("validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"validation passed: {args.pack}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
