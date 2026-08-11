#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REGISTRY_COLUMNS = (
    "Project ID",
    "Project Name",
    "Workspace Reference",
    "Current Stage",
    "Active Version",
    "Artifact State",
    "Approval Requirement",
    "Human Approval",
    "System/Template Version",
    "Last Verified",
)
REQUIRED_PATH_KEYS = {
    "system_version_record",
    "gate_map",
    "project_template",
    "project_registry",
    "template_manifest",
    "project_control",
    "stage_state",
    "knowledge_backflow",
}


@dataclass
class Finding:
    level: str
    path: Path
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a file-based team workflow system.")
    parser.add_argument("system", type=Path, help="Mother-system root.")
    parser.add_argument("--project", action="append", type=Path, help="Formal project to validate; repeatable.")
    parser.add_argument("--strict-remote", action="store_true", help="Treat a missing Git remote as an error.")
    return parser.parse_args()


def locate_contract(root: Path) -> Path:
    candidates = (root / "00-system-rules/workflow-contract.json", root / "workflow-contract.json")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("workflow-contract.json not found at root or 00-system-rules/")


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


def markdown_field(path: Path, label: str) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^-[ \t]+{re.escape(label)}:[ \t]*(.*)$", text, re.MULTILINE)
    return clean(match.group(1)) if match else None


def parse_flat_yaml(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        if key == key.lstrip():
            result[key.strip()] = clean(value)
    return result


def git_output(path: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def valid_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def nonempty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item for item in value)


def validate_contract(contract_path: Path, contract: object, findings: list[Finding]) -> None:
    if not isinstance(contract, dict):
        findings.append(Finding("ERROR", contract_path, "contract must be a JSON object"))
        return
    required = (
        "schema_version",
        "system_version",
        "template_version",
        "project_id_pattern",
        "gate_id_pattern",
        "project_qa_id_pattern",
        "gate_statuses",
        "artifact_statuses",
        "approval_requirement_statuses",
        "human_approval_statuses",
        "source_statuses",
        "representation_statuses",
        "execution_surface_statuses",
        "governance_statuses",
        "ai_coverage_statuses",
        "adoption_evidence_statuses",
        "canonical_gates",
        "paths",
        "required_project_files",
        "backflow_required_artifact_statuses",
        "release_requires_decided_approval_requirement",
    )
    for key in required:
        if key not in contract or contract[key] in (None, "", [], {}):
            findings.append(Finding("ERROR", contract_path, f"missing or empty contract key: {key}"))

    for key in ("schema_version", "system_version", "template_version"):
        value = contract.get(key)
        if isinstance(value, str) and not re.fullmatch(r"\d+\.\d+\.\d+", value):
            findings.append(Finding("ERROR", contract_path, f"{key} must use semantic version syntax"))

    enum_keys = (
        "gate_statuses",
        "artifact_statuses",
        "approval_requirement_statuses",
        "human_approval_statuses",
        "source_statuses",
        "representation_statuses",
        "execution_surface_statuses",
        "governance_statuses",
        "ai_coverage_statuses",
        "adoption_evidence_statuses",
        "backflow_required_artifact_statuses",
    )
    for key in enum_keys:
        values = contract.get(key)
        if not nonempty_string_list(values):
            findings.append(Finding("ERROR", contract_path, f"{key} must be a non-empty string list"))
        elif len(values) != len(set(values)):
            findings.append(Finding("ERROR", contract_path, f"duplicate value in {key}"))

    required_enum_values = {
        "gate_statuses": {"not-checked", "pass", "conditional-pass", "return", "blocked"},
        "artifact_statuses": {"not-recorded", "draft", "frozen", "released", "archived"},
        "approval_requirement_statuses": {"undetermined", "not-required", "required"},
        "human_approval_statuses": {"not-recorded", "not-requested", "pending", "approved", "rejected"},
        "representation_statuses": {"tacit/manual", "documented", "structured"},
        "execution_surface_statuses": {"undetermined", "local", "shared-repository", "shared-toolspace", "platform"},
        "governance_statuses": {"unmanaged", "controlled", "governed"},
        "ai_coverage_statuses": {"none", "assisted", "executable"},
        "adoption_evidence_statuses": {"designed", "online-tested", "pilot-adopted", "operationally-accepted"},
    }
    for key, required_values in required_enum_values.items():
        values = set(contract.get(key, []))
        missing_values = sorted(required_values - values)
        if missing_values:
            findings.append(Finding("ERROR", contract_path, f"{key} missing canonical values: {', '.join(missing_values)}"))

    compiled: dict[str, re.Pattern[str]] = {}
    for key in ("project_id_pattern", "gate_id_pattern", "project_qa_id_pattern"):
        value = contract.get(key)
        if not isinstance(value, str) or not value:
            continue
        try:
            compiled[key] = re.compile(value)
        except re.error as exc:
            findings.append(Finding("ERROR", contract_path, f"invalid {key}: {exc}"))

    paths = contract.get("paths")
    if not isinstance(paths, dict):
        findings.append(Finding("ERROR", contract_path, "paths must be an object"))
    else:
        missing_paths = sorted(REQUIRED_PATH_KEYS - set(paths))
        if missing_paths:
            findings.append(Finding("ERROR", contract_path, f"paths missing keys: {', '.join(missing_paths)}"))
        for key in REQUIRED_PATH_KEYS & set(paths):
            value = paths[key]
            if not isinstance(value, str) or not value or Path(value).is_absolute() or ".." in Path(value).parts:
                findings.append(Finding("ERROR", contract_path, f"paths.{key} must be a safe relative path"))

    gates = contract.get("canonical_gates")
    gate_pattern = compiled.get("gate_id_pattern")
    if not isinstance(gates, dict) or not gates:
        findings.append(Finding("ERROR", contract_path, "canonical_gates must be a non-empty object"))
    else:
        for gate_id, name in gates.items():
            if not isinstance(gate_id, str) or (gate_pattern and not gate_pattern.fullmatch(gate_id)):
                findings.append(Finding("ERROR", contract_path, f"invalid canonical Gate ID: {gate_id!r}"))
            if not isinstance(name, str) or not name.strip():
                findings.append(Finding("ERROR", contract_path, f"canonical Gate {gate_id!r} has a blank name"))

    artifacts = set(contract.get("artifact_statuses", []))
    for status in contract.get("backflow_required_artifact_statuses", []):
        if status not in artifacts:
            findings.append(Finding("ERROR", contract_path, f"unknown backflow artifact status: {status}"))
    if not isinstance(contract.get("release_requires_decided_approval_requirement"), bool):
        findings.append(
            Finding("ERROR", contract_path, "release_requires_decided_approval_requirement must be boolean")
        )

    runtime = contract.get("ai_runtime", {"enabled": False})
    if not isinstance(runtime, dict) or not isinstance(runtime.get("enabled", False), bool):
        findings.append(Finding("ERROR", contract_path, "ai_runtime must be an object with a boolean enabled field"))


def validate_approval(
    path: Path,
    requirement: str,
    approval: str,
    decision_source: str,
    contract: dict,
    findings: list[Finding],
) -> None:
    if requirement not in set(contract["approval_requirement_statuses"]):
        findings.append(Finding("ERROR", path, f"invalid or blank approval_requirement: {requirement!r}"))
        return
    if approval not in set(contract["human_approval_statuses"]):
        findings.append(Finding("ERROR", path, f"invalid or blank human_approval: {approval!r}"))
        return
    if requirement == "undetermined" and approval not in {"not-requested", "not-recorded"}:
        findings.append(Finding("ERROR", path, "undetermined approval requirement cannot carry an approval decision"))
    if requirement == "not-required" and approval != "not-requested":
        findings.append(Finding("ERROR", path, "not-required approval must use human_approval=not-requested"))
    if requirement != "undetermined" and not decision_source:
        findings.append(Finding("ERROR", path, "decided approval requirement needs approval_decision_source"))


def validate_state(
    path: Path,
    contract: dict,
    findings: list[Finding],
    *,
    template: bool,
) -> dict[str, str]:
    state = parse_flat_yaml(path)
    required_state_keys = (
        "project_id",
        "project_name",
        "system_version",
        "template_version",
        "contract_version",
        "current_stage",
        "current_node",
        "current_workitem",
        "gate_id",
        "gate_status",
        "artifact_status",
        "approval_requirement",
        "human_approval",
        "approval_decision_source",
        "representation",
        "execution_surface",
        "governance",
        "ai_coverage",
        "adoption_evidence",
        "active_deliverable",
        "active_version",
        "immutable_identity",
        "last_updated",
        "updated_by",
    )
    for key in required_state_keys:
        if key not in state:
            findings.append(Finding("ERROR", path, f"missing state key: {key}"))

    allowed = {
        "gate_status": set(contract["gate_statuses"]),
        "artifact_status": set(contract["artifact_statuses"]),
        "representation": set(contract["representation_statuses"]),
        "execution_surface": set(contract["execution_surface_statuses"]),
        "governance": set(contract["governance_statuses"]),
        "ai_coverage": set(contract["ai_coverage_statuses"]),
        "adoption_evidence": set(contract["adoption_evidence_statuses"]),
    }
    for key, values in allowed.items():
        if state.get(key, "") not in values:
            findings.append(Finding("ERROR", path, f"invalid or blank {key}: {state.get(key)!r}"))
    expected_versions = {
        "system_version": contract["system_version"],
        "template_version": contract["template_version"],
        "contract_version": contract["schema_version"],
    }
    for key, expected in expected_versions.items():
        if state.get(key) != expected:
            findings.append(Finding("ERROR", path, f"{key} {state.get(key)!r} does not match {expected!r}"))

    validate_approval(
        path,
        state.get("approval_requirement", ""),
        state.get("human_approval", ""),
        state.get("approval_decision_source", ""),
        contract,
        findings,
    )

    for key in ("current_stage", "current_node", "current_workitem", "gate_id", "active_deliverable", "active_version"):
        if not state.get(key):
            findings.append(Finding("ERROR", path, f"blank operational state field: {key}"))
    gate_id = state.get("gate_id", "")
    if gate_id and gate_id not in contract["canonical_gates"]:
        findings.append(Finding("ERROR", path, f"gate_id is not canonical: {gate_id}"))

    if not template:
        for key in ("project_id", "project_name", "last_updated", "updated_by"):
            if not state.get(key):
                findings.append(Finding("ERROR", path, f"blank project state field: {key}"))
        if state.get("last_updated") and not valid_date(state["last_updated"]):
            findings.append(Finding("ERROR", path, f"last_updated is not ISO date: {state['last_updated']}"))
        if state.get("current_stage") != "initialization":
            for key in ("owner_slot", "review_slot", "decision_slot"):
                if not state.get(key):
                    findings.append(Finding("WARN", path, f"active project has blank role field: {key}"))

    artifact = state.get("artifact_status", "")
    if artifact in {"frozen", "released"}:
        for key in ("active_version", "immutable_identity"):
            if not state.get(key):
                findings.append(Finding("ERROR", path, f"{artifact} artifact has blank {key}"))
    if artifact == "released" and contract.get("release_requires_decided_approval_requirement", False):
        requirement = state.get("approval_requirement", "")
        approval = state.get("human_approval", "")
        if requirement == "undetermined":
            findings.append(Finding("ERROR", path, "released artifact has undetermined approval requirement"))
        elif requirement == "required" and approval != "approved":
            findings.append(Finding("ERROR", path, "released artifact with required approval needs human_approval=approved"))
    return state


def validate_gate_identity(root: Path, contract: dict, findings: list[Finding]) -> None:
    canonical = contract["canonical_gates"]
    gate_pattern = re.compile(contract["gate_id_pattern"])
    qa_pattern = re.compile(contract["project_qa_id_pattern"])
    statuses = set(contract["gate_statuses"])
    for path in sorted(root.glob("**/*.md")):
        if ".git" in path.parts or path.is_symlink():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            row = cells(line)
            if len(row) < 2:
                continue
            item_id = row[0]
            if qa_pattern.fullmatch(item_id):
                continue
            if not gate_pattern.fullmatch(item_id):
                continue
            if item_id not in canonical:
                findings.append(Finding("ERROR", path, f"line {line_number}: unregistered system Gate {item_id}"))
                continue
            checkpoint = row[1]
            if checkpoint and checkpoint not in statuses and checkpoint != canonical[item_id]:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"line {line_number}: {item_id} is named {checkpoint!r}; expected {canonical[item_id]!r}",
                    )
                )


def validate_registry(root: Path, path: Path, contract: dict, findings: list[Finding]) -> dict[str, list[list[str]]]:
    rows_by_id: dict[str, list[list[str]]] = {}
    if not path.is_file():
        findings.append(Finding("ERROR", path, "project registry does not exist"))
        return rows_by_id
    text = path.read_text(encoding="utf-8")
    if "<!-- PROJECT_ROWS -->" not in text:
        findings.append(Finding("ERROR", path, "project registry marker is missing"))
    header_found = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            continue
        row = cells(line)
        if tuple(row) == REGISTRY_COLUMNS:
            header_found = True
            continue
        if row and all(re.fullmatch(r":?-{3,}:?", item) for item in row):
            continue
        if not row or row[0] in {"", "Project ID"}:
            continue
        if len(row) != len(REGISTRY_COLUMNS):
            findings.append(
                Finding("ERROR", path, f"line {line_number}: registry row has {len(row)} cells; expected {len(REGISTRY_COLUMNS)}")
            )
            continue
        project_id = row[0]
        rows_by_id.setdefault(project_id, []).append(row)
        if not re.fullmatch(contract["project_id_pattern"], project_id):
            findings.append(Finding("ERROR", path, f"line {line_number}: invalid project ID {project_id!r}"))
        if row[5] not in set(contract["artifact_statuses"]):
            findings.append(Finding("ERROR", path, f"line {line_number}: invalid artifact state {row[5]!r}"))
        validate_approval(path, row[6], row[7], "registry-reference", contract, findings)
        if row[8] != f"{contract['system_version']}/{contract['template_version']}":
            findings.append(Finding("ERROR", path, f"line {line_number}: system/template version drift: {row[8]!r}"))
        if not valid_date(row[9]):
            findings.append(Finding("ERROR", path, f"line {line_number}: Last Verified is not ISO date: {row[9]!r}"))
        reference = row[2]
        if "://" not in reference:
            target = Path(reference)
            target = target if target.is_absolute() else root / target
            if not target.exists():
                findings.append(Finding("ERROR", path, f"line {line_number}: workspace reference does not exist: {reference}"))
            else:
                state_path = target / contract["paths"]["stage_state"]
                if not state_path.is_file():
                    findings.append(Finding("ERROR", path, f"line {line_number}: registered project has no stage state"))
                else:
                    state = parse_flat_yaml(state_path)
                    validate_approval(
                        state_path,
                        state.get("approval_requirement", ""),
                        state.get("human_approval", ""),
                        state.get("approval_decision_source", ""),
                        contract,
                        findings,
                    )
                    expected = (
                        state.get("project_id", ""),
                        state.get("project_name", ""),
                        state.get("current_stage", ""),
                        state.get("active_version", ""),
                        state.get("artifact_status", ""),
                        state.get("approval_requirement", ""),
                        state.get("human_approval", ""),
                    )
                    actual = (row[0], row[1], row[3], row[4], row[5], row[6], row[7])
                    if actual != expected:
                        findings.append(Finding("ERROR", path, f"line {line_number}: registry state drifts from project state"))
    if not header_found:
        findings.append(Finding("ERROR", path, "project registry header does not match the contract schema"))
    for project_id, rows in rows_by_id.items():
        if len(rows) > 1:
            findings.append(Finding("ERROR", path, f"duplicate project registry rows: {project_id}"))
    return rows_by_id


def validate_ai_runtime(root: Path, contract: dict, findings: list[Finding]) -> None:
    runtime = contract.get("ai_runtime", {"enabled": False})
    if not runtime.get("enabled", False):
        return
    for key in ("system_entrypoints", "project_entrypoints", "required_capabilities"):
        if not isinstance(runtime.get(key), list):
            findings.append(Finding("ERROR", root, f"ai_runtime.{key} must be a list"))
    for key in ("pre_write_check", "post_write_check"):
        if not isinstance(runtime.get(key), str) or not runtime[key].strip():
            findings.append(Finding("ERROR", root, f"enabled AI runtime needs ai_runtime.{key}"))
    for relative in runtime.get("system_entrypoints", []):
        if not isinstance(relative, str) or not (root / relative).is_file():
            findings.append(Finding("ERROR", root, f"missing AI system entrypoint: {relative!r}"))
    for capability in runtime.get("required_capabilities", []):
        if not isinstance(capability, dict) or not capability.get("id") or not capability.get("path"):
            findings.append(Finding("ERROR", root, "each required capability needs id and path"))
            continue
        capability_path = Path(capability["path"]).expanduser()
        if not capability_path.exists():
            findings.append(Finding("ERROR", root, f"required capability is not installed/discoverable: {capability['id']}"))


def validate_system(root: Path, contract: dict, findings: list[Finding]) -> dict[str, list[list[str]]]:
    paths = contract["paths"]
    version_record = root / paths["system_version_record"]
    if not version_record.is_file():
        findings.append(Finding("ERROR", version_record, "system version record does not exist"))
    else:
        expected_versions = {
            "System version": contract["system_version"],
            "Template version": contract["template_version"],
            "Contract/schema version": contract["schema_version"],
        }
        for label, expected in expected_versions.items():
            if markdown_field(version_record, label) != expected:
                findings.append(Finding("ERROR", version_record, f"{label} does not match {expected!r}"))
    gate_map = root / paths["gate_map"]
    if not gate_map.is_file():
        findings.append(Finding("ERROR", gate_map, "canonical Gate map does not exist"))
    template = root / paths["project_template"]
    if not template.is_dir():
        findings.append(Finding("ERROR", template, "runtime project template does not exist"))
    else:
        for relative in contract["required_project_files"]:
            if not (template / relative).is_file():
                findings.append(Finding("ERROR", template, f"template missing required project file: {relative}"))
        state_path = template / paths["stage_state"]
        if state_path.is_file():
            validate_state(state_path, contract, findings, template=True)
    registry_rows = validate_registry(root, root / paths["project_registry"], contract, findings)
    validate_gate_identity(root, contract, findings)
    validate_ai_runtime(root, contract, findings)
    return registry_rows


def validate_git(project: Path, findings: list[Finding], strict_remote: bool) -> None:
    if not (project / ".git").exists():
        findings.append(Finding("WARN", project, "no Git repository; record an equivalent immutable baseline"))
        return
    count = git_output(project, "rev-list", "--count", "HEAD")
    if not count or count == "0":
        findings.append(Finding("ERROR", project, "Git repository has no baseline commit"))
    if not git_output(project, "remote"):
        findings.append(Finding("ERROR" if strict_remote else "WARN", project, "no remote backup is configured"))


def validate_backflow(project: Path, relative: str, findings: list[Finding]) -> None:
    path = project / relative
    for label in (
        "Source project ID",
        "Source repository / workspace",
        "Source version / tag / snapshot",
        "Closure date",
    ):
        if not markdown_field(path, label):
            findings.append(Finding("ERROR", path, f"eligible project has blank backflow field: {label}"))


def validate_project(
    root: Path,
    project: Path,
    contract: dict,
    registry_rows: dict[str, list[list[str]]],
    findings: list[Finding],
    strict_remote: bool,
) -> None:
    if not project.is_dir():
        findings.append(Finding("ERROR", project, "project path does not exist or is not a directory"))
        return
    missing = [relative for relative in contract["required_project_files"] if not (project / relative).is_file()]
    for relative in missing:
        findings.append(Finding("ERROR", project, f"missing required project file: {relative}"))
    if missing:
        return

    validate_git(project, findings, strict_remote)
    paths = contract["paths"]
    state_path = project / paths["stage_state"]
    manifest_path = project / paths["template_manifest"]
    control_path = project / paths["project_control"]
    state = validate_state(state_path, contract, findings, template=False)

    manifest_values = {
        "Project ID": state.get("project_id", ""),
        "Project name": state.get("project_name", ""),
        "System version": contract["system_version"],
        "Template version": contract["template_version"],
        "Contract/schema version": contract["schema_version"],
    }
    for label, expected in manifest_values.items():
        if markdown_field(manifest_path, label) != expected:
            findings.append(Finding("ERROR", manifest_path, f"{label} does not match {expected!r}"))
    creation_date = markdown_field(manifest_path, "Creation date") or ""
    if not valid_date(creation_date):
        findings.append(Finding("ERROR", manifest_path, f"Creation date is not ISO date: {creation_date!r}"))

    control_values = {
        "Project ID": state.get("project_id", ""),
        "Project name": state.get("project_name", ""),
        "System version": contract["system_version"],
        "Template version": contract["template_version"],
        "Contract/schema version": contract["schema_version"],
        "Last updated": state.get("last_updated", ""),
        "Updated by": state.get("updated_by", ""),
        "Current stage": state.get("current_stage", ""),
        "Current node / work item": f"{state.get('current_node', '')} / {state.get('current_workitem', '')}",
        "Current Gate ID": state.get("gate_id", ""),
        "Gate result": state.get("gate_status", ""),
        "Artifact state": state.get("artifact_status", ""),
        "Approval requirement": state.get("approval_requirement", ""),
        "Human approval": state.get("human_approval", ""),
        "Approval decision source": state.get("approval_decision_source", ""),
        "Current active deliverable": state.get("active_deliverable", ""),
        "Current active version": state.get("active_version", ""),
        "Representation": state.get("representation", ""),
        "Execution surface": state.get("execution_surface", ""),
        "Governance": state.get("governance", ""),
        "AI coverage": state.get("ai_coverage", ""),
        "Adoption evidence": state.get("adoption_evidence", ""),
    }
    for label, expected in control_values.items():
        if markdown_field(control_path, label) != expected:
            findings.append(Finding("ERROR", control_path, f"{label} does not match {expected!r}"))
    workspace_reference = markdown_field(control_path, "Workspace reference") or ""
    if not workspace_reference or Path(workspace_reference).resolve() != project.resolve():
        findings.append(Finding("ERROR", control_path, "Workspace reference does not resolve to this project"))

    project_id = state.get("project_id", "")
    if not re.fullmatch(contract["project_id_pattern"], project_id):
        findings.append(Finding("ERROR", state_path, f"invalid or blank project_id: {project_id!r}"))
    rows = registry_rows.get(project_id, [])
    if len(rows) != 1:
        findings.append(Finding("ERROR", root / paths["project_registry"], f"project needs exactly one registry row: {project_id}"))
    else:
        row = rows[0]
        expected_row = (
            project_id,
            state.get("project_name", ""),
            state.get("current_stage", ""),
            state.get("active_version", ""),
            state.get("artifact_status", ""),
            state.get("approval_requirement", ""),
            state.get("human_approval", ""),
            f"{contract['system_version']}/{contract['template_version']}",
        )
        actual_row = (row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8])
        if actual_row != expected_row:
            findings.append(Finding("ERROR", root / paths["project_registry"], f"registry state drifts from project state: {project_id}"))
        reference = Path(row[2])
        registered_path = reference if reference.is_absolute() else root / reference
        if registered_path.resolve() != project.resolve():
            findings.append(Finding("ERROR", root / paths["project_registry"], f"registry path does not resolve to project: {project_id}"))

    artifact = state.get("artifact_status", "")
    if artifact in set(contract["backflow_required_artifact_statuses"]):
        validate_backflow(project, paths["knowledge_backflow"], findings)

    runtime = contract.get("ai_runtime", {"enabled": False})
    if runtime.get("enabled", False):
        for relative in runtime.get("project_entrypoints", []):
            if not isinstance(relative, str) or not (project / relative).is_file():
                findings.append(Finding("ERROR", project, f"missing AI project entrypoint: {relative!r}"))


def main() -> int:
    args = parse_args()
    root = args.system.resolve()
    findings: list[Finding] = []
    try:
        contract_path = locate_contract(root)
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {root}: {exc}")
        return 1

    validate_contract(contract_path, contract, findings)
    registry_rows: dict[str, list[list[str]]] = {}
    if not any(item.level == "ERROR" for item in findings):
        try:
            validate_git(root, findings, args.strict_remote)
            registry_rows = validate_system(root, contract, findings)
            for project in args.project or []:
                validate_project(
                    root,
                    project.resolve(),
                    contract,
                    registry_rows,
                    findings,
                    args.strict_remote,
                )
        except (KeyError, TypeError, OSError, ValueError) as exc:
            findings.append(Finding("ERROR", contract_path, f"validator could not interpret the contract safely: {exc}"))

    for item in findings:
        try:
            label = item.path.relative_to(root.parent)
        except ValueError:
            label = item.path
        print(f"[{item.level}] {label}: {item.message}")
    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARN" for item in findings)
    print(f"Validated system and {len(args.project or [])} project(s): {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
