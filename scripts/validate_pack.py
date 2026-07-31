#!/usr/bin/env python3
"""Validate the release invariants of a manifest-driven asset pack."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FILES = ("manifest.json", "installation.md", "usage.md", "license.md")
VALID_STATUSES = {"draft", "needs_revision", "approved", "rejected"}
ASSET_PATH_FIELDS = ("reference", "model_source", "preview", "review", "provenance")


def is_safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def validate(root: Path, release: bool = False) -> list[str]:
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
    if not isinstance(manifest.get("provenance"), list):
        errors.append("manifest provenance must be a list")
    provenance_ids = {
        record.get("asset_id")
        for record in manifest.get("provenance", [])
        if isinstance(record, dict) and record.get("asset_id")
    }
    if release:
        if manifest.get("status") != "approved":
            errors.append("release mode requires pack status: approved")
        if not manifest["assets"]:
            errors.append("release mode requires at least one asset")
        if not manifest.get("provenance"):
            errors.append("release mode requires at least one provenance record")
        for key in ("target_runtime", "license_profile", "demo_entry"):
            if not isinstance(manifest.get(key), str) or not manifest[key].strip():
                errors.append(f"release mode requires non-empty manifest field: {key}")
        if not isinstance(manifest.get("supported_versions"), list) or not manifest["supported_versions"]:
            errors.append("release mode requires supported_versions")
        demo_entry = manifest.get("demo_entry")
        if demo_entry and (not is_safe_relative_path(demo_entry) or not (root / demo_entry).is_file()):
            errors.append(f"release mode requires a real demo_entry file: {demo_entry}")

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
        for field in ASSET_PATH_FIELDS:
            if asset.get(field) and not is_safe_relative_path(asset[field]):
                errors.append(f"asset {asset_id or index} has unsafe path for {field}: {asset[field]}")
        if asset.get("status") == "approved":
            for field in ("preview", "provenance"):
                if not asset.get(field):
                    errors.append(f"approved asset {asset_id} missing {field}")
        if release and asset.get("status") == "approved":
            if asset_id not in provenance_ids:
                errors.append(f"approved asset {asset_id} has no matching provenance record")
            for field in ASSET_PATH_FIELDS:
                path_value = asset.get(field)
                if path_value and not (root / path_value).is_file():
                    errors.append(f"approved asset {asset_id} missing file for {field}: {path_value}")
        if release and asset.get("status") != "approved":
            errors.append(f"release mode requires approved asset: {asset_id or index}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", type=Path)
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    errors = validate(args.pack, release=args.release)
    if errors:
        print("validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"validation passed: {args.pack}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
