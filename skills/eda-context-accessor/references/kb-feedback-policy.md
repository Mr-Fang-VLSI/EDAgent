# KB Feedback Policy

## Goal

After scoped KB/tool retrieval, emit an explicit recommendation about whether the current knowledge base should change.

## Allowed Decisions

Use exactly one of:
- `none`: current KB is adequate for this task.
- `maintain`: KB structure/linking/index is stale or inconsistent and should be repaired.
- `update`: existing KB content is directionally right but needs refreshed evidence or rewritten status.
- `overturn`: current KB guidance is contradicted strongly enough that the old claim should no longer be treated as valid.
- `add`: the task exposed a missing knowledge item that deserves a new KB entry.

## Decision Heuristics

Choose `maintain` when:
- links, paths, references, or indexes are stale,
- the content is still conceptually right but operationally broken.

Choose `update` when:
- the claim remains valid in structure,
- but newer evidence changes status, thresholds, confidence, or operating conditions.

Choose `overturn` when:
- retrieved evidence directly invalidates a KB claim or policy,
- and downstream work would be misled if the old claim remains authoritative.

Choose `add` when:
- no KB entry covers a recurring question, workflow, failure mode, or validated finding.

Choose `none` when:
- no KB change is justified by the current scoped retrieval.

## Output Requirement

Always emit:
1. `kb_feedback_decision`
2. `kb_feedback_reason`
3. the KB files or missing areas affected by that decision
