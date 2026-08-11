#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_workflow_system.py")
FORBIDDEN_NAME_CHARACTERS = set("/\\|`<>:\n\r\t")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a formal project from a workflow-system template.")
    parser.add_argument("system", type=Path, help="Mother-system root.")
    parser.add_argument("--id", required=True, help="Project ID matching the system contract.")
    parser.add_argument("--name", required=True, help="Human-readable project name.")
    parser.add_argument("--workspace", type=Path, help="Existing parent directory; defaults to the mother-system parent.")
    parser.add_argument(
        "--allow-inside-system",
        action="store_true",
        help="Explicitly allow project placement inside the mother system.",
    )
    git_group = parser.add_mutually_exclusive_group()
    git_group.add_argument(
        "--init-git",
        action="store_true",
        help="Explicitly initialize and commit a project Git repository after validation.",
    )
    git_group.add_argument(
        "--no-git",
        action="store_true",
        help="Deprecated compatibility flag; Git is no longer initialized by default.",
    )
    return parser.parse_args()


def locate_contract(root: Path) -> Path:
    for path in (root / "00-system-rules/workflow-contract.json", root / "workflow-contract.json"):
        if path.is_file():
            return path
    raise FileNotFoundError("workflow-contract.json not found")


def clean(value: str) -> str:
    cleaned = value.strip().strip("`").strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] == '"':
        try:
            return str(json.loads(cleaned))
        except json.JSONDecodeError:
            pass
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] == "'":
        return cleaned[1:-1]
    return cleaned


def cells(line: str) -> list[str]:
    return [clean(cell) for cell in line.strip().strip("|").split("|")]


def parse_flat_yaml(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        if key == key.lstrip():
            result[key.strip()] = clean(value)
    return result


def validate_project_name(raw: str) -> str:
    if raw != raw.strip():
        raise ValueError("Project name cannot start or end with whitespace.")
    if not raw or raw in {".", ".."} or len(raw) > 80:
        raise ValueError("Project name must contain 1-80 safe characters.")
    if any(character in FORBIDDEN_NAME_CHARACTERS or ord(character) < 32 or ord(character) == 127 for character in raw):
        raise ValueError("Project name contains a path, Markdown-table, markup, or control character.")
    if raw.endswith("."):
        raise ValueError("Project name cannot end with a dot.")
    return raw


def replace_markdown_field(path: Path, label: str, value: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        rf"^(-[ \t]+{re.escape(label)}:[ \t]*).*$",
        rf"\g<1>{value}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise RuntimeError(f"Field not found in {path}: {label}")
    path.write_text(updated, encoding="utf-8")


def replace_yaml_field(path: Path, key: str, value: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        rf"^{re.escape(key)}:.*$",
        f"{key}: {value}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise RuntimeError(f"Field not found in {path}: {key}")
    path.write_text(updated, encoding="utf-8")


def mark_checklist_item(path: Path, text_label: str, checked: bool) -> None:
    text = path.read_text(encoding="utf-8")
    marker = "x" if checked else " "
    updated, count = re.subn(
        rf"^- \[[ xX]\] {re.escape(text_label)}$",
        f"- [{marker}] {text_label}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise RuntimeError(f"Checklist item not found in {path}: {text_label}")
    path.write_text(updated, encoding="utf-8")


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        stream.write(text)
        temporary = Path(stream.name)
    temporary.chmod(mode)
    temporary.replace(path)


def run_git(project: Path, *args: str) -> None:
    result = subprocess.run(["git", "-C", str(project), *args], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def run_validator(root: Path, project: Path | None = None) -> str:
    command = [sys.executable, str(VALIDATOR), str(root)]
    if project is not None:
        command.extend(["--project", str(project)])
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    if result.returncode != 0:
        raise RuntimeError(f"Workflow-system validation failed:\n{output}")
    return output


def register_project(root: Path, contract: dict, state: dict[str, str], target: Path) -> tuple[Path, str]:
    registry = root / contract["paths"]["project_registry"]
    original = registry.read_text(encoding="utf-8")
    project_id = state["project_id"]
    for line in original.splitlines():
        row = cells(line)
        if row and row[0] == project_id:
            raise RuntimeError(f"Project already registered: {project_id}")
    marker = "<!-- PROJECT_ROWS -->"
    if marker not in original:
        raise RuntimeError("Project registry marker is missing")
    reference = Path(os.path.relpath(target, root)).as_posix()
    row = (
        f"| {project_id} | {state['project_name']} | `{reference}` | {state['current_stage']} | "
        f"{state['active_version']} | {state['artifact_status']} | {state['approval_requirement']} | "
        f"{state['human_approval']} | {contract['system_version']}/{contract['template_version']} | "
        f"{state['last_updated']} |\n"
    )
    atomic_write(registry, original.replace(marker, row + marker, 1))
    return registry, original


def main() -> int:
    args = parse_args()
    root = args.system.resolve()
    try:
        contract = json.loads(locate_contract(root).read_text(encoding="utf-8"))
        run_validator(root)
        name = validate_project_name(args.name)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, RuntimeError) as exc:
        print(f"Cannot initialize project: {exc}", file=sys.stderr)
        return 2

    if not re.fullmatch(contract["project_id_pattern"], args.id):
        print(f"Project ID does not match {contract['project_id_pattern']}", file=sys.stderr)
        return 2

    workspace = (args.workspace or root.parent).resolve()
    if not workspace.is_dir():
        print(f"Workspace parent does not exist or is not a directory: {workspace}", file=sys.stderr)
        return 2
    source = root / contract["paths"]["project_template"]
    target = workspace / f"{args.id}-{name}"
    if not source.is_dir():
        print(f"Project template does not exist: {source}", file=sys.stderr)
        return 2
    if target.exists():
        print(f"Target already exists: {target}", file=sys.stderr)
        return 2
    if target.is_relative_to(root) and not args.allow_inside_system:
        print("Refusing project placement inside the mother system without --allow-inside-system.", file=sys.stderr)
        return 2

    control_rel = contract["paths"]["project_control"]
    manifest_rel = contract["paths"]["template_manifest"]
    state_rel = contract["paths"]["stage_state"]
    today = date.today().isoformat()
    initialize_git = args.init_git and not args.no_git
    registry: Path | None = None
    registry_original: str | None = None
    try:
        shutil.copytree(source, target)
        control = target / control_rel
        manifest = target / manifest_rel
        state = target / state_rel
        markdown_values = (
            (control, "Project ID", args.id),
            (control, "Project name", name),
            (control, "Workspace reference", str(target)),
            (control, "System version", f"`{contract['system_version']}`"),
            (control, "Template version", f"`{contract['template_version']}`"),
            (control, "Contract/schema version", f"`{contract['schema_version']}`"),
            (control, "Last updated", today),
            (control, "Updated by", "create_project.py"),
            (control, "Current stage", "initialization"),
            (control, "Current node / work item", "project-setup / initialize-governance"),
            (control, "Current Gate ID", "`WF-G1`"),
            (control, "Gate result", "`not-checked`"),
            (control, "Artifact state", "`draft`"),
            (control, "Approval requirement", "`undetermined`"),
            (control, "Human approval", "`not-requested`"),
            (control, "Approval decision source", ""),
            (control, "Current active deliverable", "project-workspace"),
            (control, "Current active version", "v0.1-project-init"),
            (control, "Representation", "structured"),
            (control, "Execution surface", "undetermined"),
            (control, "Governance", "controlled"),
            (control, "AI coverage", "none"),
            (control, "Adoption evidence", "designed"),
            (manifest, "Project ID", args.id),
            (manifest, "Project name", name),
            (manifest, "System version", f"`{contract['system_version']}`"),
            (manifest, "Template version", f"`{contract['template_version']}`"),
            (manifest, "Contract/schema version", f"`{contract['schema_version']}`"),
            (manifest, "Creation date", today),
        )
        for path, label, value in markdown_values:
            replace_markdown_field(path, label, value)

        state_values = {
            "project_id": args.id,
            "project_name": json.dumps(name, ensure_ascii=False),
            "system_version": contract["system_version"],
            "template_version": contract["template_version"],
            "contract_version": contract["schema_version"],
            "current_stage": "initialization",
            "current_node": "project-setup",
            "current_workitem": "initialize-governance",
            "gate_id": "WF-G1",
            "gate_status": "not-checked",
            "artifact_status": "draft",
            "approval_requirement": "undetermined",
            "human_approval": "not-requested",
            "approval_decision_source": "",
            "representation": "structured",
            "execution_surface": "undetermined",
            "governance": "controlled",
            "ai_coverage": "none",
            "adoption_evidence": "designed",
            "active_deliverable": "project-workspace",
            "active_version": "v0.1-project-init",
            "last_updated": today,
            "updated_by": "create_project.py",
        }
        for key, value in state_values.items():
            replace_yaml_field(state, key, value)

        parsed_state = parse_flat_yaml(state)
        registry, registry_original = register_project(root, contract, parsed_state, target)
        run_validator(root, target)

        mark_checklist_item(manifest, "Fill the project control page and stage state.", True)
        mark_checklist_item(manifest, "Establish a Git commit/tag or equivalent immutable baseline.", initialize_git)
        mark_checklist_item(manifest, "Register the project in the mother system.", True)
        mark_checklist_item(manifest, "Run the workflow-system validator.", True)

        if initialize_git:
            run_git(target, "init", "-b", "main")
            run_git(target, "add", "-A")
            run_git(target, "commit", "-m", "Initialize formal project workspace")
        validation_output = run_validator(root, target)
    except Exception as exc:
        if registry is not None and registry_original is not None:
            try:
                atomic_write(registry, registry_original)
            except OSError as restore_error:
                print(f"Registry rollback failed: {restore_error}", file=sys.stderr)
        if target.exists():
            shutil.rmtree(target)
        print(f"Project creation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Created {target}")
    print(f"Registered {args.id} in {contract['paths']['project_registry']}")
    if validation_output:
        print(validation_output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
