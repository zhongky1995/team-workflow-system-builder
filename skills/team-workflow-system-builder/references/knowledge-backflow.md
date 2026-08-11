# Knowledge Backflow And Closure

Use this reference when closing a project, updating the mother system, or extracting reusable assets.

## Contents

1. Closure boundary
2. Provenance
3. Reuse and privacy
4. Knowledge destinations
5. Completion Gate

## Closure Boundary

Separate:

- Project archive: project facts, evidence, decisions, drafts, releases, and unresolved items.
- Mother-system backflow: reusable methods, templates, decision rules, cases, benchmarks, and failure lessons.

Do not copy a full project workspace into the mother system. Do not treat file cleanup as project closure.

## Provenance

Every backflow item should record:

- Source project ID and repository/workspace.
- Source artifact and version/tag/snapshot.
- Evidence path or decision record.
- Extraction date and owner.
- What was abstracted and what was removed.
- Target knowledge type and destination.
- Index update status.
- Knowledge status: `provisional`, `validated`, `challenged`, or `deprecated`.
- Validation evidence, applicability boundary, and challenge/replacement chain.

`provisional` means the item has a traceable source but has not been independently adopted or confirmed. `validated` requires named evidence beyond the producing project’s self-description. If the source project or outcome is later rejected, mark the item `challenged` until its reusable claim is re-evaluated. Do not delete historical knowledge merely to hide the challenge.

## Reuse And Privacy

Before backflow, determine:

- Confidentiality or client restriction.
- Copyright and quotation boundary.
- Whether names, metrics, screenshots, or identifiers need removal.
- Whether the item can be reused as a method, pattern, anonymized case, or only internal warning.
- Whether human approval is required, who decided that requirement, and the decision source.

Prefer mechanisms over copied content. Preserve enough provenance to verify the lesson without leaking protected project material.

## Knowledge Destinations

| Type | Destination example |
|---|---|
| Template improvement | Runtime template source and migration record |
| SOP or method | Methods/protocols library |
| Decision rule | Governance or decision-rule index |
| Reusable case | Anonymized case library |
| Failure lesson | Failure-lessons library |
| Benchmark | Metrics/benchmark register with source period |
| Skill improvement | Skill instruction, reference, asset, script, or eval |

## Completion Gate

Closure is complete only when:

- Final and unresolved items are separated.
- Active/frozen/released versions are identifiable.
- Archive index and retrospective exist.
- Each reusable item has provenance and a destination.
- Each reusable item has a lifecycle status and validation/applicability evidence.
- Restricted content is excluded or approved.
- Mother-system indexes are updated.
- Follow-up owners and deadlines are recorded.
- Approval requirement, human approval, and their human decision source remain explicit.

Use `assets/templates/knowledge-backflow-card.md` as the starting point.
