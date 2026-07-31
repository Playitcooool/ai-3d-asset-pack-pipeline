#!/usr/bin/env python3
"""Create a minimal, manifest-driven asset pack workspace."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not result:
        raise ValueError("pack name must contain letters or numbers")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack_name")
    parser.add_argument("--output", type=Path, default=Path("."))
    args = parser.parse_args()

    pack_id = slug(args.pack_name)
    root = args.output / pack_id
    if root.exists():
        raise SystemExit(f"refusing to overwrite existing directory: {root}")

    for directory in ("src", "exports", "demo", "previews", "assets"):
        (root / directory).mkdir(parents=True)

    manifest = {
        "pack_id": pack_id,
        "pack_name": args.pack_name,
        "version": "0.1.0",
        "status": "draft",
        "primary_format": "procedural-typescript",
        "assets": [],
        "provenance": [],
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for name, body in {
        "installation.md": f"# {args.pack_name}\n\nAdd installation steps here.\n",
        "usage.md": f"# Usage\n\nDocument how to use the {args.pack_name} assets.\n",
        "license.md": "# License\n\nAdd the commercial license and attribution requirements here.\n",
        "changelog.md": "# Changelog\n\n## 0.1.0\n\n- Initial draft.\n",
    }.items():
        (root / name).write_text(body)

    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
