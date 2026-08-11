#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an external scoped baseline for a non-Git repair.")
    parser.add_argument("target", type=Path, help="Repair target root.")
    parser.add_argument("--output-dir", required=True, type=Path, help="External baseline directory.")
    parser.add_argument("--name", required=True, help="Safe baseline name.")
    parser.add_argument("--include", action="append", required=True, help="Relative file/directory to archive; repeatable.")
    parser.add_argument("--exclude-note", action="append", default=[], help="Recorded exclusion or no-edit boundary.")
    parser.add_argument("--allow-whole-target", action="store_true", help="Explicitly allow --include .")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    output_dir = args.output_dir.resolve()
    if not target.is_dir():
        print(f"Target is not a directory: {target}", file=sys.stderr)
        return 2
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.name):
        print("Name may contain only letters, digits, dot, underscore, and hyphen.", file=sys.stderr)
        return 2
    if output_dir == target or output_dir.is_relative_to(target):
        print("Output directory must be outside the repair target.", file=sys.stderr)
        return 2

    selected: list[tuple[Path, Path]] = []
    seen: set[str] = set()
    for raw in args.include:
        relative = Path(raw)
        if relative.is_absolute() or ".." in relative.parts:
            print(f"Include must be a safe relative path: {raw}", file=sys.stderr)
            return 2
        if relative == Path(".") and not args.allow_whole_target:
            print("Refusing a whole-target archive without --allow-whole-target.", file=sys.stderr)
            return 2
        source = (target / relative).resolve()
        if not source.is_relative_to(target):
            print(f"Include escapes target: {raw}", file=sys.stderr)
            return 2
        if not source.exists():
            print(f"Include does not exist: {raw}", file=sys.stderr)
            return 2
        arcname = source.relative_to(target)
        key = arcname.as_posix()
        if key not in seen:
            selected.append((source, arcname))
            seen.add(key)

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive = output_dir / f"{args.name}_before_{timestamp}.tar.gz"
    manifest = output_dir / f"{args.name}_before_{timestamp}.json"
    try:
        with tarfile.open(archive, "w:gz") as bundle:
            for source, arcname in selected:
                bundle.add(source, arcname=arcname, recursive=True)
        archive_hash = sha256(archive)
        payload = {
            "created_at_utc": timestamp,
            "target": str(target),
            "archive": str(archive),
            "sha256": archive_hash,
            "included_paths": [arcname.as_posix() for _, arcname in selected],
            "excluded_or_no_edit_boundaries": args.exclude_note,
            "restore_rule": "Preserve the repaired state first, then extract this archive at the recorded target root.",
        }
        manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        archive.unlink(missing_ok=True)
        manifest.unlink(missing_ok=True)
        print(f"Baseline creation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Archive: {archive}")
    print(f"Manifest: {manifest}")
    print(f"SHA-256: {archive_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
