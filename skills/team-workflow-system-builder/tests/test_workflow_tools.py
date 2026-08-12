from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"


def run_script(name: str, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *(str(arg) for arg in args)],
        text=True,
        capture_output=True,
        check=False,
    )


def output(result: subprocess.CompletedProcess[str]) -> str:
    return "\n".join(part for part in (result.stdout, result.stderr) if part)


class WorkflowToolTests(unittest.TestCase):
    def create_system(self, root: Path, profile: str = "minimal") -> Path:
        system = root / "mother-system"
        result = run_script("create_system.py", system, "--profile", profile)
        self.assertEqual(result.returncode, 0, output(result))
        return system

    def create_project(self, root: Path, system: Path, project_id: str = "OPS-2026-001", name: str = "Demo") -> Path:
        workspace = root / "projects"
        workspace.mkdir()
        result = run_script(
            "create_project.py",
            system,
            "--id",
            project_id,
            "--name",
            name,
            "--workspace",
            workspace,
        )
        self.assertEqual(result.returncode, 0, output(result))
        return workspace / f"{project_id}-{name}"

    def enable_valid_ai_runtime(self, root: Path, system: Path) -> Path:
        entrypoint = system / "AGENTS.md"
        entrypoint.write_text("# Runtime entrypoint\n", encoding="utf-8")
        capability = root / "installed-research-skill"
        capability.mkdir()
        (capability / "SKILL.md").write_text("# Installed capability\n", encoding="utf-8")

        contract_path = system / "00-system-rules/workflow-contract.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        contract["ai_runtime"].update(
            {
                "enabled": True,
                "system_entrypoints": ["AGENTS.md"],
                "project_entrypoints": [],
                "required_capabilities": [{"id": "research-skill", "path": str(capability)}],
                "pre_write_check": "python tools/preflight.py",
                "post_write_check": "python tools/validate.py",
            }
        )
        contract_path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")

        dispatch_path = system / contract["ai_runtime"]["dispatch_registry"]
        dispatch = {
            "schema_version": "0.1.0",
            "adoption_evidence": "online-tested",
            "work_item_inventory": ["WORK-01", "WORK-02"],
            "excluded_work_items": [
                {"id": "WORK-02", "reason": "Human-only policy decision", "human_owner": "Final Decision"}
            ],
            "work_items": [
                {
                    "id": "WORK-01",
                    "stage": "planning",
                    "deliverable": "review-draft",
                    "truth_source": "02-workflow/work-item-map.md#WORK-01",
                    "route": "specialist-optional",
                    "ai_action": "draft",
                    "inputs": ["approved brief"],
                    "allowed_actions": ["create a review draft"],
                    "expected_outputs": ["review draft"],
                    "human_boundary": "The accountable owner approves the plan and release.",
                    "pre_write_checks": ["brief is current"],
                    "post_write_checks": ["draft cites the active baseline"],
                    "failure_behavior": "Return a bounded draft and list missing inputs.",
                    "writeback_targets": ["project work-item record"],
                    "capability_route": {
                        "build_route_id": "artifact-production",
                        "candidate_ids": ["research-skill"],
                        "discovery_tags": ["research"],
                        "selected_id": "research-skill",
                        "required": True,
                        "fallback": "Stop specialist execution and return a visible handoff.",
                    },
                }
            ],
        }
        dispatch_path.write_text(json.dumps(dispatch, indent=2) + "\n", encoding="utf-8")
        return dispatch_path

    def test_create_project_keeps_registry_and_state_coherent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root, "standard")
            registry_path = system / "09-governance/project-registry.md"
            registry_mode = registry_path.stat().st_mode & 0o777
            project = self.create_project(root, system, name="治理试点")
            result = run_script("validate_workflow_system.py", system, "--project", project)
            self.assertEqual(result.returncode, 0, output(result))

            state = (project / "02-stage-state/stage-state.yaml").read_text(encoding="utf-8")
            registry = registry_path.read_text(encoding="utf-8")
            self.assertIn("current_stage: initialization", state)
            self.assertIn("approval_requirement: undetermined", state)
            self.assertIn("human_approval: not-requested", state)
            self.assertIn("| initialization | v0.1-project-init | draft | undetermined | not-requested |", registry)
            self.assertFalse((project / ".git").exists())
            self.assertEqual(registry_path.stat().st_mode & 0o777, registry_mode)

    def test_unsafe_project_name_is_rejected_before_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root)
            workspace = root / "projects"
            workspace.mkdir()
            result = run_script(
                "create_project.py",
                system,
                "--id",
                "OPS-2026-002",
                "--name",
                "Bad|Name",
                "--workspace",
                workspace,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("control character", output(result))
            self.assertFalse((workspace / "OPS-2026-002-Bad|Name").exists())
            registry = (system / "09-governance/project-registry.md").read_text(encoding="utf-8")
            self.assertNotIn("OPS-2026-002", registry)

    def test_missing_contract_key_fails_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root)
            contract_path = system / "00-system-rules/workflow-contract.json"
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            del contract["gate_id_pattern"]
            contract_path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")

            result = run_script("validate_workflow_system.py", system)
            combined = output(result)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing or empty contract key: gate_id_pattern", combined)
            self.assertNotIn("Traceback", combined)

    def test_enabled_ai_runtime_validates_complete_dispatch_and_installed_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root)
            self.enable_valid_ai_runtime(root, system)
            result = run_script("validate_workflow_system.py", system)
            self.assertEqual(result.returncode, 0, output(result))

    def test_enabled_ai_runtime_rejects_unaccounted_work_item(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root)
            dispatch_path = self.enable_valid_ai_runtime(root, system)
            dispatch = json.loads(dispatch_path.read_text(encoding="utf-8"))
            dispatch["work_item_inventory"].append("WORK-03")
            dispatch_path.write_text(json.dumps(dispatch, indent=2) + "\n", encoding="utf-8")
            result = run_script("validate_workflow_system.py", system)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("work-item inventory is not fully accounted: WORK-03", output(result))

    def test_human_owner_route_cannot_execute_human_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root)
            dispatch_path = self.enable_valid_ai_runtime(root, system)
            dispatch = json.loads(dispatch_path.read_text(encoding="utf-8"))
            item = dispatch["work_items"][0]
            item["route"] = "human-owner"
            item["ai_action"] = "execute-restricted"
            dispatch_path.write_text(json.dumps(dispatch, indent=2) + "\n", encoding="utf-8")
            result = run_script("validate_workflow_system.py", system)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("human-owner route cannot execute the human decision", output(result))

    def test_registry_drift_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root)
            project = self.create_project(root, system)
            registry_path = system / "09-governance/project-registry.md"
            registry = registry_path.read_text(encoding="utf-8")
            registry_path.write_text(registry.replace("| initialization |", "| planning |", 1), encoding="utf-8")

            result = run_script("validate_workflow_system.py", system, "--project", project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("registry state drifts from project state", output(result))

    @unittest.skipUnless(hasattr(os, "symlink"), "symbolic links are unavailable")
    def test_package_rejects_symbolic_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root)
            os.symlink("/etc/hosts", system / "leak-hosts")
            archive = root / "system.zip"
            result = run_script("package_system.py", system, "--output", archive)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symbolic links", output(result))
            self.assertFalse(archive.exists())

    def test_valid_package_contains_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            system = self.create_system(root)
            executable = system / "tools/check.sh"
            executable.parent.mkdir(exist_ok=True)
            executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            executable.chmod(0o755)
            archive = root / "system.zip"
            result = run_script("package_system.py", system, "--output", archive)
            self.assertEqual(result.returncode, 0, output(result))
            with zipfile.ZipFile(archive) as bundle:
                names = bundle.namelist()
                packaged_mode = (bundle.getinfo(f"{system.name}/tools/check.sh").external_attr >> 16) & 0o777
            self.assertIn(f"{system.name}/MANIFEST.sha256", names)
            self.assertFalse(any(name.endswith(".git") or "/.git/" in name for name in names))
            self.assertEqual(packaged_mode, 0o755)

            second = run_script("package_system.py", system, "--output", archive)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("without --overwrite", output(second))


if __name__ == "__main__":
    unittest.main()
