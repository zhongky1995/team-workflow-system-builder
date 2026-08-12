# Target Runtime Capability Dispatch

Use this reference when the target team workflow—not the transformation effort itself—will receive AI requests, route work to specialist Skills, or preserve human-only work through one runtime entrypoint.

## Two Different Routing Layers

| Layer | Purpose | Canonical contract | Owner |
|---|---|---|---|
| Build-time specialist routing | Route architecture, knowledge-system, artifact, platform, or Skill-packaging work needed to build or repair the operating system | `specialist-routing-registry.json` | `team-workflow-system-builder` and the active host agent |
| Target runtime dispatch | Route the target team's real work items after the operating workflow is online | Target system `ai-work-item-dispatch.json` or an equivalent platform registry | Target workflow owner and accountable human owners |

Never use the build-time registry as a production dispatcher. It knows transformation capabilities, not the target team's domain work items, project state, accepted inputs, Gates, or decision rights.

## What Must Be Accounted For

Inventory every formal work item in the selected target slice. For each item choose exactly one accounting result:

- `runtime-routed`: the runtime can receive or coordinate the item;
- `excluded`: the item remains outside AI runtime, with a reason and named human owner.

`runtime-routed` does not mean autonomous. A routed item may still be `human-owner` and permit only assistance, drafting, or recommendation.

Every routed item records:

- work-item ID, Stage, deliverable, and operational truth source;
- route: `workflow-owner`, `specialist-optional`, or `human-owner`;
- AI action: `assist`, `draft`, `recommend`, `execute-reversible`, or `execute-restricted`;
- accepted inputs and allowed actions;
- expected outputs and writeback targets;
- human boundary and decisions AI cannot make;
- pre-write and post-write checks;
- failure behavior and recovery path;
- capability route, candidates, selected installed capability, and fallback;
- adoption evidence and last verification when the registry is operated.

Do not copy the target business method, template body, or project facts into this registry. Link to their canonical sources.

## Capability Lifecycle

Keep these states distinct:

```text
candidate
  -> selected for this work item
  -> packaged
  -> installed / discoverable
  -> invoked from the real entrypoint
  -> result reintegrated and accepted
```

A candidate ID is routing intent, not proof of any later state. If a selected specialist is required, record its installed path or platform identity in the target runtime contract. If the capability is optional or unavailable, execute the recorded fallback and keep the missing specialist work visible.

## Runtime Registry Shape

Use `assets/templates/ai-work-item-dispatch.json` for the bundled file-based profile. The top-level fields are:

- `schema_version`;
- `adoption_evidence`;
- `work_item_inventory`;
- `excluded_work_items`;
- `work_items`.

Each `work_items` entry uses this shape:

```json
{
  "id": "WORK-01",
  "stage": "planning",
  "deliverable": "approved-plan",
  "truth_source": "02-workflow/work-item-map.md#WORK-01",
  "route": "specialist-optional",
  "ai_action": "draft",
  "inputs": ["approved brief", "current source baseline"],
  "allowed_actions": ["create a review draft"],
  "expected_outputs": ["review draft"],
  "human_boundary": "The accountable owner approves the plan and release.",
  "pre_write_checks": ["brief and source baseline are current"],
  "post_write_checks": ["draft cites the active baseline"],
  "failure_behavior": "Return a bounded draft and list missing inputs.",
  "writeback_targets": ["project work-item record"],
  "capability_route": {
    "build_route_id": "artifact-production",
    "candidate_ids": ["documents:documents"],
    "discovery_tags": ["document production"],
    "selected_id": "",
    "required": false,
    "fallback": "Return approved content plus a visible format handoff."
  }
}
```

`build_route_id` is provenance to the construction-time decision, not permission to use the build registry at runtime.

## Selection Rules

1. Apply the human-decision hard stop before capability matching.
2. Prefer the target workflow owner when the work is ordinary governance or domain execution already covered by the runtime entrypoint.
3. Route only the bounded specialist portion; retain the target work-item owner and Gate meaning.
4. Verify that a selected Skill exists in the active catalog and read it before invocation.
5. Pass minimum context: accepted facts, source/version baseline, exact task, allowed actions, no-edit regions, human boundary, validation, and integration destination.
6. Reconcile the result with the target workflow before state, version, Gate, release, or backflow changes.
7. If no suitable capability exists, use the explicit fallback. Do not silently absorb specialist work or fabricate installation evidence.

## When To Create A Separate Workflow Skill

Create a separate runtime Skill only when the bounded work item:

- has stable inputs, outputs, authority, failure behavior, and writeback;
- has reached at least `online-tested` through the real entrypoint;
- has realistic positive, negative, unavailable-capability, and human-boundary evals;
- avoids duplicating target-system truth sources;
- reduces context or execution risk enough to justify another package and route.

Do not split one Skill per Stage merely because the lifecycle has multiple Stages. Keep orchestration in one entrypoint until an independently verifiable capability boundary is proven.

## Validation

For the bundled file profile, enabling `ai_runtime` requires:

- a dispatch registry with complete inventory accounting;
- valid route and AI-action classes;
- nonempty inputs, actions, outputs, human boundary, pre/post checks, failure behavior, and writeback targets;
- selected required capabilities present in `ai_runtime.required_capabilities` and installed at their recorded paths;
- system/project entrypoints and pre/post checks;
- a real-entrypoint forward test that proves human-only decisions remain non-executable.

Structure validation proves contract completeness, not adoption. Report `designed`, `online-tested`, `pilot-adopted`, and `operationally-accepted` only from separate evidence.
