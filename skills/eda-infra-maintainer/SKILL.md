---
name: eda-infra-maintainer
description: Maintain and evolve the EDA infrastructure stack (agent policy, knowledge base, tool registry, and skill system) with auditable guardrails and minimal-risk updates.
---

# EDA Infra Maintainer

## When to use

Use this skill when the user asks to:
1. improve/repair infrastructure (`knowledge_base`, `tool_registry`, `skills`, `agent` policy),
2. harden governance and reliability checks,
3. add new infrastructure capability for future research loops,
4. maintain full-chain research workflow infrastructure (`init_research_chain`, `research_chain_guard`, chain templates/skills).

Use `eda-artifact-hygiene-maintainer` instead when the task is primarily artifact cleanup:
- merge duplicated KB/tool/log artifacts,
- archive or delete stale artifacts,
- normalize inaccurate naming.

## Scope Boundary

This skill owns infrastructure governance and integrity.
It does not own domain experiment conclusions (timing/power/route/model physics).

This skill is the direct workflow owner for infrastructure maintenance and development tasks.
`eda-loop` is not the default wrapper here; use it only when infrastructure work explicitly includes one bounded governed execution stage.

## Expected Downstream Consumers

Typical consumers include:
- `workflow-router` when routing exposes a structural gap,
- `eda-context-accessor` when KB feedback requires infra maintenance,
- execution and theory skills when governance, manifest, or policy drift must be repaired,
- `eda-artifact-hygiene-maintainer` when cleanup surfaces a policy-level inconsistency.

## Knowledge And Tool Interaction

1. Treat `AGENTS.md`, the knowledge base, the tool registry, and the skill manifest as governed infrastructure state that must stay mutually consistent.
2. Use `eda-context-accessor` when infrastructure work needs shared KB/tool retrieval artifacts that downstream skills should reuse.
3. Treat non-`none` `kb_feedback_decision` from utility or execution skills as an actionable maintenance input and classify it as `maintain`, `update`, `overturn`, or `add` work.
4. Run guard/audit tools before and after changes, then write the resulting artifact paths into the maintenance report.

## Inputs

Provide or derive:
1. maintenance mode (`use`, `maintain`, or `develop`),
2. touched infra surfaces (`AGENTS.md`, `skills`, `docs/knowledge_base`, `docs/tool_registry`, scripts, manifests, or routing),
3. required guard/audit scope,
4. expected artifact outputs,
5. whether any bounded execution stage must be delegated to `eda-loop`.

## Outputs

Return or update:
- guard/audit artifacts under `slurm_logs/00_meta/`,
- touched governance/skill/KB/tool files,
- maintenance report with rollback trigger,
- explicit reference-topology decision for every touched skill,
- explicit statement of whether `eda-loop` was `not_used` or `delegated_stage`.

## Hard rules

1. Do not mix infrastructure governance with domain result claims.
2. Do not change comparison policy locks silently.
3. If critical guard checks fail, block promotion and fix first.
4. If utility logic is duplicated across multiple skills, centralize it instead of patching the same interaction pattern repeatedly.
5. Do not route routine infrastructure maintenance through `eda-loop` unless the task truly contains a governed execution substep.

## Operational References

1. Load `references/maintenance-checklist.md` when executing any infra maintenance change and you need the mandatory pre/post sequence.
2. Load `references/workflow-owner-usage.md` when deciding whether this skill should stay the direct workflow owner or delegate one bounded execution stage to `eda-loop`.
3. Load `references/baseline-guard-and-audit.md` when selecting which guard, audit, and tool-query commands to run before or after an infra update.
4. Load `references/skill-reference-topology-policy.md` when a change touches `SKILL.md` or `references/*.md` layout and you need a merge-vs-split decision.
5. Load `references/skill-type-patterns.md` when classifying a touched skill as `theory-analysis`, `execution`, or `utility`.
6. Load `references/utility-skill-maintenance-pattern.md` when the task is specifically reorganizing utility skills or horizontal capability boundaries.
7. Load `references/architecture-change-validation.md` when the task changes skill architecture, routing, or workflow ownership and you need to record expected benefits plus a later validation plan.
8. Load `references/infrastructure-reporting.md` when writing the change summary, rollback trigger, and artifact-path report.
