# Agent Responsibilities and Skill Boundaries

## Purpose
This file is the top-level execution policy for this repository.
Agent-level responsibilities must live here, not inside individual skills.

## Agent Owns (Global)
1. Interpret user intent, constraints, and risk level.
2. Require an explicit routing decision before execution, using `workflow-router` as the canonical routing policy owner.
3. Enforce cross-skill policies (baseline lock, comparison fairness, promotion rules).
4. Decide whether to recurse into another loop after retrospective evidence.
5. Decide whether a gap should be fixed in skill/docs/scripts now.
6. Keep user communication contract consistent (artifacts, assumptions, open risks).

## Skills Own (Local)
1. Deterministic, reusable workflows inside a bounded scope.
2. Domain-specific analysis/execution logic.
3. Skill-local references/scripts/templates.

## Skills Must Not Own
1. Repo-wide entry policy.
2. Cross-skill governance and recursion policy.
3. Global "self-modify skill system" requirements by default.
4. User-facing orchestration contract for all task types.

## Skill Architecture Principle

The repo should keep three things separable:
1. capability: what a skill knows how to do,
2. knowledge: KB docs, paper-derived summaries, and background evidence,
3. tools: reusable scripts and registry entries.

Design rules:
1. Skills should own capability and routing inside a bounded scope.
2. Knowledge should live in the knowledge base or paper-derived artifacts, not be duplicated as large static background inside `SKILL.md`.
3. Tools should live in the tool registry and scripts, not be embedded as ad hoc one-off logic inside multiple skills.
4. Skills should link to knowledge and tools explicitly, so updating the KB or tool registry updates skill behavior through those links rather than through duplicated text.
5. Reused horizontal logic should be extracted into utility skills before it is repeated across multiple execution or theory skills.

## Standard Agent Flow
1. Classify request type and required evidence level.
2. Run `workflow-router` when skill/workflow selection is non-trivial or needs to be stated explicitly.
3. Use the routing result to identify one `workflow_owner_skill`.
4. If high-cost/high-risk, run `eda-theory-veto` before expensive execution inside the selected workflow.
5. Invoke the selected workflow owner directly:
- `eda-loop` only for one scoped execution workflow,
- `eda-research-chain` for multi-stage research workflow,
- utility owners such as `eda-infra-maintainer` or `eda-artifact-hygiene-maintainer` for maintenance workflows,
- specialist/theory skills directly when no execution wrapper is needed.
6. Use `eda-loop` only when it is the selected workflow owner or when another workflow owner explicitly delegates one governed execution stage to it.
7. If batch/experiment completed, run `eda-retro` only when the active workflow needs post-experiment mechanism and next-step decision.
8. Apply minimal maintenance updates only when a repeated gap is confirmed.

## Mandatory Routing Disclosure

When workflow or skill selection is performed, the agent must explicitly disclose the routing result to the user before or at the start of execution.

Minimum disclosure fields:
1. `Detected workflow`
2. `Workflow owner`
3. `Skills used`
4. `New workflow decision = reuse_existing | create_new_workflow | no_new_workflow`

If routing was trivial and `workflow-router` was not explicitly invoked, the agent must still disclose the effective workflow and selected skills whenever non-trivial work is about to proceed.

## Deployment Onboarding Contract
For a newly deployed environment (or first interaction in a new repo), agent must do this before normal execution:
1. Give a brief self-introduction (role, capability boundary, and what it can automate).
2. Clearly state that full usage mode needs permission to create/maintain infrastructure folders and files:
- `docs/knowledge_base/`
- `docs/tool_registry/`
- `skills/`
- `scripts/common/`
- `slurm_logs/00_meta/`
3. Ask user to confirm whether this infrastructure bootstrap is allowed.
4. Ask user for current research direction and top optimization goal/constraints.
5. If user does not allow bootstrap, run in constrained mode and avoid persistent infra writes.

## Pre-Submit Hard Gate
1. Any long/batch experiment submission must have a fresh theory-veto artifact (`GO` or constrained `CONDITIONAL`).
2. `NO-GO` blocks submission by default; proceed only with explicit `veto_overridden` marking.

## Routing Policy
`workflow-router` is the only skill that owns reusable workflow classification and skill-selection policy.

Agent-level rule:
1. `AGENTS.md` defines governance, not request-pattern matrices.
2. `workflow-router` owns the canonical routing references, workflow-owner contract, and output format.
3. Routing must identify one `workflow_owner_skill`; the owner is not implicitly `eda-loop`.
4. `eda-loop` consumes a scoped execution brief; it does not own the repo routing matrix and is not the default wrapper for every workflow.
5. No compatibility entry skill is required; routing policy lives directly in `workflow-router`.

## Early-Round Testcase Policy (BSPDN Goal)
1. For early hypothesis rounds, prioritize `net-dense + small-scale` testcases to maximize information per wall-clock.
2. Use density/size gate from latest usage TSV (default: high `selected_ratio_pct`, bounded `total_nets`) before admitting large designs.
3. Defer large designs to confirmation rounds after at least one stable small-case mechanism signal is observed.

## Goal Focus Lock
1. Core optimization target is backside signal-layer aware placement/route behavior (dynamic-power and timing/area tradeoff).
2. PDN is a boundary constraint for legality/stability, not a primary optimization objective in this project stage.

## Infrastructure Stewardship Modes
Agent must support three explicit modes for the core infrastructure (`knowledge_base`, `tool_registry`, `skills`):

1. Use mode:
- execute user experiment/research task using existing infrastructure,
- do not change governance unless a blocking gap is discovered.

2. Maintain mode:
- fix integrity/drift issues in existing infrastructure (broken links, stale routing, manifest inconsistency),
- preserve current policy intent and minimize behavioral change.

3. Develop mode:
- introduce new capabilities (new skill, new guard script, new governance rule),
- require explicit boundary definition, validation evidence, and rollback condition.

## Mandatory Infrastructure Checks
For maintain/develop requests, run:
1. `python3 scripts/common/infra_stack_guard.py --out-prefix <prefix>`
2. `python3 scripts/common/skill_system_audit.py --out-prefix <prefix>`
3. `python3 scripts/common/tool_catalog.py query <keywords>`
4. `python3 scripts/common/unified_kb_query.py build` (refresh retrieval index for `docs/knowledge_base`)

If any critical check fails, block promotion claims until fixed.

## Infrastructure Versioning Contract
1. Tool registry entries must carry lifecycle/version metadata (`tool_id`, `lifecycle`, `version`, `owner`) in catalog output.
2. Skills manifest must carry `skill_version`, `interface_version`, and `depends_on_tools` (bound to `tool_id`, not script path).
3. Deprecation must specify migration target (`replacement_tool_id`) before a tool is retired.

## Mandatory Output Contract (Infrastructure Work)
Every infrastructure interaction must leave:
1. changed file list,
2. one guard artifact (`infra_stack_guard` summary path),
3. one skill-system audit artifact,
4. explicit `risk + rollback trigger` note.

## Mandatory Output Contract (Execution / Research Work)

For any non-trivial execution, research, or maintenance interaction, the user-facing response should also include:
1. detected workflow,
2. workflow owner skill,
3. selected skill set,
4. whether a new workflow was needed.

## Skill Boundary Table
| Skill | Owns | Does Not Own |
|---|---|---|
| `workflow-router` | Workflow classification, skill shortlist construction, and new-skill decision policy | Repo-wide governance, execution artifacts, domain implementation |
| `eda-loop` | Scoped single-task execution ownership and delegated governed execution stages | Global entry policy, routing policy ownership, non-execution workflow ownership, recursion governance, global self-update policy |
| `eda-research-chain` | End-to-end research-chain workflow ownership for idea-to-validation flow | Global policy ownership and generic single-task execution ownership |
| `eda-knowledge-explorer` | Knowledge exploration and evidence-gap mapping | Method implementation and final validation claims |
| `eda-idea-debate-lab` | Brainstorming and adversarial idea refinement | Experiment execution and production code changes |
| `eda-hypothesis-experiment-designer` | Hypothesis-to-experiment design with pass/fail criteria | Running production implementation changes directly |
| `eda-method-implementer` | Method implementation with integration contract and validation handoff | Final promotion decision without validation evidence |
| `bspdn-goal-driver` | Staged optimization toward explicit PPA goals with milestone gating | One-shot final-goal claim without intermediate evidence |
| `eda-infra-maintainer` | Infrastructure maintenance/development workflow for KB/tool/skills stack | Domain experiment logic and physics/model conclusions |
| `eda-artifact-hygiene-maintainer` | KB/tool/log artifact cleanup, duplicate merge, stale archive/delete, and naming normalization | Governance policy ownership and domain conclusion changes |
| `eda-knowledge-gate-maintainer` | Gate hygiene utility and maintenance logging | Task planning, cross-skill routing decisions |
| Domain skills (`bscost-*`, `gt3-*`, `delay-*`, paper/pdf, slides) | Domain logic and artifacts | Repo-wide orchestration decisions |

## Consolidation Decision
1. Agent duties formerly duplicated in legacy entry shims and `eda-loop` are moved here.
2. Skill-routing duties formerly duplicated across `AGENTS.md`, `eda-loop`, and compatibility docs are consolidated into `workflow-router`.
3. `eda-loop` remains the primary owner for one scoped execution workflow, not the universal owner for all workflows.
4. Legacy compatibility shim `eda-chief` has been removed from the active skill system.

## Change Policy
1. Prefer updating specialized domain skills before orchestration skills.
2. Update `eda-loop` only for repeated execution-level gaps.
3. Update this `AGENTS.md` when governance/routing policy changes.
