#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS = SKILL_ROOT / "assets/templates"
VALIDATOR = Path(__file__).with_name("validate_workflow_system.py")

SYSTEM_FILES = {
    "system-version.md": "00-system-rules/system-version.md",
    "workflow-contract.json": "00-system-rules/workflow-contract.json",
    "workflow-gate-map.md": "02-workflow/stage-gate-map.md",
    "project-registry.md": "09-governance/project-registry.md",
}

REQUIRED_PROJECT_FILES = {
    "template-manifest.md": "template-manifest.md",
    "project-control.md": "project-control.md",
    "stage-state.yaml": "02-stage-state/stage-state.yaml",
    "decision-log.md": "06-decisions-risks-changes/decision-log.md",
    "risk-log.md": "06-decisions-risks-changes/risk-log.md",
    "change-log.md": "06-decisions-risks-changes/change-log.md",
    "archive-index.md": "07-archive-backflow/archive-index.md",
    "retrospective.md": "07-archive-backflow/retrospective.md",
    "knowledge-backflow-card.md": "07-archive-backflow/knowledge-backflow-card.md",
}

STANDARD_PROJECT_FILES = {
    "intake-card.md": "00-brief/intake-card.md",
    "scenario-card.md": "00-brief/scenario-card.md",
    "client-alignment-card.md": "01-context/client-alignment-card.md",
    "material-reading-plan.md": "01-context/material-reading-plan.md",
    "work-item-record.md": "03-work-records/work-item-record.md",
    "deliverable-review-checklist.md": "03-work-records/deliverable-review-checklist.md",
    "active-version-index.md": "04-deliverables/active-version-index.md",
    "source-register.md": "05-evidence/source-register.md",
}

SYSTEM_DIRECTORIES = (
    "01-team-context",
    "03-role-matrix",
    "04-deliverable-standards/review-checklists",
    "06-sandbox",
    "07-source-and-evidence",
    "08-knowledge-base/reusable-cases",
    "08-knowledge-base/methods",
    "08-knowledge-base/failure-lessons",
    "08-knowledge-base/indexes",
    "09-governance/migrations",
    "tools",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new mother-system from the bundled canonical assets.")
    parser.add_argument("target", type=Path, help="New mother-system path; it must not already exist.")
    parser.add_argument(
        "--profile",
        choices=("minimal", "standard"),
        default="minimal",
        help="minimal copies only contract-required project files; standard adds common operating records.",
    )
    return parser.parse_args()


def copy_files(target: Path, mapping: dict[str, str], prefix: Path | None = None) -> None:
    base = target if prefix is None else target / prefix
    for source_name, relative in mapping.items():
        source = ASSETS / source_name
        destination = base / relative
        if not source.is_file():
            raise FileNotFoundError(f"Bundled asset is missing: {source}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    if target.exists():
        print(f"Refusing to overwrite an existing path: {target}", file=sys.stderr)
        return 2

    try:
        target.mkdir(parents=True)
        copy_files(target, SYSTEM_FILES)
        template = Path("05-templates/project-workspace-template")
        copy_files(target, REQUIRED_PROJECT_FILES, template)
        if args.profile == "standard":
            copy_files(target, STANDARD_PROJECT_FILES, template)
            for relative in SYSTEM_DIRECTORIES:
                (target / relative).mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(target)],
            text=True,
            capture_output=True,
            check=False,
        )
        output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
        if result.returncode != 0:
            raise RuntimeError(f"Generated system failed validation:\n{output}")
    except Exception as exc:
        if target.exists():
            shutil.rmtree(target)
        print(f"System creation failed and was rolled back: {exc}", file=sys.stderr)
        return 1

    print(f"Created {target} with profile={args.profile}")
    if output:
        print(output)
    print("Customize the accepted workflow, then establish a Git or external immutable baseline before project work.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
