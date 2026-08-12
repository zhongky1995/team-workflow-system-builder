#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "references/specialist-routing-registry.json"
ALLOWED_MODES = {"self", "specialist", "human-owner", "human-or-specialist"}
REQUIRED_ROUTE_FIELDS = {
    "id",
    "priority",
    "mode",
    "when",
    "exclusions",
    "candidate_skills",
    "discovery_tags",
    "required_inputs",
    "expected_outputs",
    "human_boundary",
    "validation",
    "integration_destination",
    "fallback",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the team workflow specialist routing registry.")
    parser.add_argument("registry", nargs="?", type=Path, default=DEFAULT_REGISTRY)
    return parser.parse_args()


def nonempty_string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [f"cannot load registry: {exc}"]

    if data.get("owner_skill") != "team-workflow-system-builder":
        errors.append("owner_skill must be team-workflow-system-builder")
    if data.get("scope") != "transformation-build-time":
        errors.append("scope must be transformation-build-time")
    if data.get("not_for") != "target-workflow-runtime-dispatch":
        errors.append("not_for must be target-workflow-runtime-dispatch")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(data.get("registry_version", ""))):
        errors.append("registry_version must use semantic version syntax")

    policy = data.get("selection_policy")
    if not isinstance(policy, dict):
        errors.append("selection_policy must be an object")
    else:
        if policy.get("decompose_composite_request") is not True:
            errors.append("selection_policy must decompose composite requests")
        for field in ("steps", "candidate_availability"):
            if not nonempty_string_list(policy.get(field)) or not policy[field]:
                errors.append(f"selection_policy.{field} must be a non-empty string list")

    routes = data.get("routes")
    if not isinstance(routes, list) or not routes:
        return errors + ["routes must be a non-empty list"]

    route_ids: list[str] = []
    priorities: list[int] = []
    for index, route in enumerate(routes, start=1):
        label = f"route[{index}]"
        if not isinstance(route, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = sorted(REQUIRED_ROUTE_FIELDS - set(route))
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")
        route_id = route.get("id")
        if not isinstance(route_id, str) or not re.fullmatch(r"[a-z0-9-]+", route_id):
            errors.append(f"{label}.id must be lowercase hyphen-case")
        else:
            route_ids.append(route_id)
            label = route_id
        priority = route.get("priority")
        if not isinstance(priority, int) or priority < 0:
            errors.append(f"{label}.priority must be a non-negative integer")
        else:
            priorities.append(priority)
        mode = route.get("mode")
        if mode not in ALLOWED_MODES:
            errors.append(f"{label}.mode must be one of {sorted(ALLOWED_MODES)}")
        for field in ("when", "required_inputs", "expected_outputs", "validation"):
            if not nonempty_string_list(route.get(field)) or not route[field]:
                errors.append(f"{label}.{field} must be a non-empty string list")
        for field in ("exclusions", "discovery_tags"):
            if not nonempty_string_list(route.get(field)):
                errors.append(f"{label}.{field} must be a string list")
        for field in ("human_boundary", "integration_destination", "fallback"):
            if not isinstance(route.get(field), str) or not route[field].strip():
                errors.append(f"{label}.{field} must be a non-empty string")

        candidates = route.get("candidate_skills")
        if not isinstance(candidates, list):
            errors.append(f"{label}.candidate_skills must be a list")
            candidates = []
        candidate_ids: list[str] = []
        for candidate in candidates:
            if not isinstance(candidate, dict):
                errors.append(f"{label} candidate must be an object")
                continue
            candidate_id = candidate.get("id")
            if not isinstance(candidate_id, str) or not re.fullmatch(r"[A-Za-z0-9._:-]+", candidate_id):
                errors.append(f"{label} candidate id is invalid")
            else:
                candidate_ids.append(candidate_id)
            if not isinstance(candidate.get("use_when"), str) or not candidate["use_when"].strip():
                errors.append(f"{label} candidate use_when must be non-empty")
        if len(candidate_ids) != len(set(candidate_ids)):
            errors.append(f"{label} candidate Skill IDs must be unique")
        if mode == "human-owner" and candidates:
            errors.append(f"{label} human-owner route must not list candidate Skills")
        if mode in {"self", "specialist"} and not candidates:
            errors.append(f"{label} {mode} route must list at least one candidate Skill")
        if mode == "specialist" and not route.get("discovery_tags"):
            errors.append(f"{label} specialist route must include discovery_tags for fallback discovery")

    if len(route_ids) != len(set(route_ids)):
        errors.append("route IDs must be unique")
    if len(priorities) != len(set(priorities)):
        errors.append("route priorities must be unique")
    resolution = data.get("resolution_order")
    if not isinstance(resolution, list) or resolution != route_ids:
        errors.append("resolution_order must exactly match route order")
    if priorities != sorted(priorities, reverse=True):
        errors.append("routes must be ordered by descending priority")
    if "workflow-governance-self" not in route_ids:
        errors.append("registry must contain workflow-governance-self")
    if "human-policy-authority" not in route_ids:
        errors.append("registry must contain human-policy-authority")
    return errors


def main() -> int:
    args = parse_args()
    errors = validate(args.registry.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    data = json.loads(args.registry.read_text(encoding="utf-8"))
    print(f"Routing registry valid: {len(data['routes'])} routes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
