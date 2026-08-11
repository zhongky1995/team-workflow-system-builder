#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


EXCLUDED_PARTS = {".git", "__MACOSX", "__pycache__", ".pytest_cache", ".mypy_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip", ".tar", ".tgz", ".gz"}
VALIDATOR = Path(__file__).with_name("validate_workflow_system.py")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a deterministic workflow-system ZIP.")
    parser.add_argument("system", type=Path, help="Mother-system root.")
    parser.add_argument("--output", type=Path, help="Output ZIP path; defaults beside the system root.")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace an existing regular output file.")
    return parser.parse_args()


def locate_contract(root: Path) -> Path:
    for path in (root / "00-system-rules/workflow-contract.json", root / "workflow-contract.json"):
        if path.is_file():
            return path
    raise FileNotFoundError("workflow-contract.json not found")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def include(path: Path, root: Path, output: Path) -> bool:
    if path.resolve() == output:
        return False
    relative = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if path.name == ".DS_Store" or path.name.startswith("._") or path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def reject_symlinks(root: Path) -> list[Path]:
    return [path for path in sorted(root.rglob("*")) if path.is_symlink()]


def validate_system(root: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(root)],
        text=True,
        capture_output=True,
        check=False,
    )
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    return result.returncode == 0, output


def main() -> int:
    args = parse_args()
    root = args.system.resolve()
    if not root.is_dir():
        print(f"System root is not a directory: {root}", file=sys.stderr)
        return 2
    try:
        contract = json.loads(locate_contract(root).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot load workflow contract: {exc}", file=sys.stderr)
        return 2

    output = (args.output or root.parent / f"{root.name}-v{contract['system_version']}.zip").resolve()
    if output.is_symlink():
        print(f"Refusing to overwrite a symlink output: {output}", file=sys.stderr)
        return 2
    if output.exists() and not args.overwrite:
        print(f"Refusing to overwrite an existing output without --overwrite: {output}", file=sys.stderr)
        return 2
    symlinks = reject_symlinks(root)
    if symlinks:
        print("Refusing to package a system containing symbolic links:", file=sys.stderr)
        for path in symlinks:
            print(f"- {path.relative_to(root)}", file=sys.stderr)
        return 2
    valid, validation_output = validate_system(root)
    if validation_output:
        print(validation_output)
    if not valid:
        print("Packaging stopped because workflow-system validation failed.", file=sys.stderr)
        return 1

    prefix = root.name
    payloads: list[tuple[str, bytes, int]] = []
    manifest: list[str] = []
    for path in sorted(root.rglob("*")):
        if not include(path, root, output):
            continue
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        mode = path.stat().st_mode & 0o777
        payloads.append((f"{prefix}/{relative}", data, mode))
        manifest.append(f"{sha256(data)}  {relative}")
    manifest_data = ("\n".join(manifest) + "\n").encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for archive_name, data, mode in payloads:
            info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100000 | mode) << 16
            archive.writestr(info, data)
        info = zipfile.ZipInfo(f"{prefix}/MANIFEST.sha256", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, manifest_data)

    print(f"Created {output}")
    print(f"Files: {len(payloads)}; archive SHA-256: {sha256(output.read_bytes())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
