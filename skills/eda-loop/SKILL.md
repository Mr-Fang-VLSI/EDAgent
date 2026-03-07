---
name: eda-loop
description: "Execute one scoped EDA task under governed gates: run bootstrap checks, validate artifacts, and return execution evidence."
---

# EDA Loop

## Role Boundary

`eda-loop` is the scoped execution workflow owner.

It owns:
- governed execution for one concrete task,
- submission hygiene,
- artifact validation,
- post-run closeout.

It does not own:
- global entry policy,
- non-execution workflow ownership,
- cross-turn recursion policy,
- global self-update policy for the full skill system.

`eda-loop` should be used only when:
1. it is the selected workflow owner for one bounded execution task, or
2. another workflow owner explicitly delegates one governed execution stage to it.

## Use This Skill When

Use `eda-loop` for experiment, debug, flow, baseline, handoff, monitoring, or infrastructure tasks that already have a scoped execution brief and need explicit gates and artifacts.

## Inputs

Provide or derive:
1. scoped objective,
2. target design/config set,
3. required output artifacts,
4. comparison-policy lock if a claim/comparison is requested.
5. selected skill set or explicit statement that no additional skill routing is needed.

## Knowledge And Tool Interaction

1. If the task needs shared KB retrieval or shared tool-reuse evidence, delegate that work to `eda-context-accessor` instead of re-specifying retrieval logic locally.
2. If `eda-context-accessor` returns `kb_feedback_decision != none`, record that feedback in the execution summary and route KB/infrastructure follow-up to `eda-infra-maintainer` when the change is not purely local.
3. Keep `eda-loop` focused on execution hygiene:
- run `scripts/common/knowledge_gate.sh` for governed execution startup,
- update `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`,
- update `docs/knowledge_base/90_HYPOTHESIS_VALIDATION_LOG.md` when a hypothesis was actually tested.

## Execution Rules

1. Announce selected skills and first action.
2. Execute fully unless the user explicitly asks for plan-only behavior.
3. Keep artifact paths explicit.
4. Immediately report monitor/manifest/job ids after submission.
5. Do not close a submission task before monitoring visibility exists.
6. For algorithmic claims, enforce `vanilla_replace` as primary baseline.

## Outputs

Return or update:
- canonical monitor path,
- canonical manifest path,
- key artifact paths,
- execution verdict,
- next constrained action.

## Operational References

Load only the parts needed for the current task:
1. Load `references/eda-loop-checklist.md` when starting or closing a normal `eda-loop` execution and you need the full bootstrap/pre-submit/post-run checklist.
2. Load `references/execution-gates.md` when the task involves submission gating, route/CTS preflight, testcase-backed DC/Innovus checks, or root-cause mode for non-convergence.
3. Load `references/output-and-stop-policy.md` when deciding whether the task is complete, whether reporting is sufficient, or whether a hard-stop condition blocks closeout.
4. Load `references/postrun-improvement.md` when the current loop exposed a repeated execution gap and you need to decide the smallest acceptable improvement action.
