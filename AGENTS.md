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

## Skill Naming And Grouping Principle
1. A skill should be identifiable from its name by both:
- primary function,
- and approximate architectural level or family.
2. Preferred naming signal:
- workflow/control-plane owners: names such as `workflow-*`, `workflow-scoped-execution`, `workflow-research-chain`, or equivalent clearly owner-like forms,
- utility/horizontal skills: names such as `eda-*-maintainer`, `eda-*-curator`, `eda-*-accessor`, `git-*`,
- domain/specialist skills: names such as `gt3-*`, `bscost-*`, `delay-*`, `rtl-*`, `academic-*`.
3. If flat naming stops being sufficiently discriminative, the system should introduce category subfolders rather than keep adding ambiguous peer directories.
4. New skills should therefore satisfy at least one of:
- the name alone clearly signals function and level,
- or the skill is placed under a category grouping that supplies the missing level/function context.
5. Do not add new skills with generic names that require reading the body to understand whether they are workflow owners, utilities, or domain specialists.

## Workflow Owner Stability Principle
1. Skills that serve as `workflow_owner_skill` are part of the middle control plane and should remain relatively stable.
2. When new functionality is needed, prefer implementing it by:
- updating lower-layer specialist skills,
- adding or refining utility skills,
- or extending reusable tools/scripts,
before changing the workflow-owner skill itself.
3. Change a workflow-owner skill directly only when:
- its orchestration contract is genuinely wrong,
- its owner/delegate boundary is incorrect,
- or the user-visible workflow semantics must change.
4. Do not use workflow-owner skills as the default place to accumulate new domain logic, parsing logic, or one-off execution detail.
5. Adoption monitoring must treat materially revised workflow-owner skills as high-priority review targets because instability at this layer affects many downstream tasks.

## Standard Agent Flow
1. Classify request type and required evidence level.
2. Run `workflow-router` when skill/workflow selection is non-trivial or needs to be stated explicitly.
3. Use the routing result to identify one `workflow_owner_skill`.
4. If high-cost/high-risk, run `control-theory-veto` before expensive execution inside the selected workflow.
5. If a batch/experiment finished and reusable empirical knowledge should be lifted from logs, run `eda-experiment-phenomenology-analyst` before retrospective or future veto use.
6. Invoke the selected workflow owner directly:
- `workflow-scoped-execution` only for one scoped execution workflow,
- `workflow-research-chain` for multi-stage research workflow,
- utility owners such as `eda-infra-maintainer` or `eda-artifact-hygiene-maintainer` for maintenance workflows,
- specialist/theory skills directly when no execution wrapper is needed.
7. Use `workflow-scoped-execution` only when it is the selected workflow owner or when another workflow owner explicitly delegates one governed execution stage to it.
8. If batch/experiment completed, run `control-postrun-retro` only when the active workflow needs post-experiment mechanism and next-step decision.
9. Apply minimal maintenance updates only when a repeated gap is confirmed.

## Theory-Practice Coupling Rule
1. Theory-oriented skills must not rely only on papers, formulas, or KB policy when relevant local experiment evidence already exists.
2. When local runs have produced reusable `result/conclusion/experience` artifacts, theory-oriented skills should consume them through `eda-experiment-phenomenology-analyst` or downstream artifacts that preserve that layer split.
3. If theory and repeated experiment experience conflict, the contradiction must be surfaced explicitly and treated as a gating input rather than ignored.

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
3. Routing must identify one `workflow_owner_skill`; the owner is not implicitly `workflow-scoped-execution`.
4. `workflow-scoped-execution` consumes a scoped execution brief; it does not own the repo routing matrix and is not the default wrapper for every workflow.
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
| `workflow-scoped-execution` | Scoped single-task execution ownership and delegated governed execution stages | Global entry policy, routing policy ownership, non-execution workflow ownership, recursion governance, global self-update policy |
| `workflow-research-chain` | End-to-end research-chain workflow ownership for idea-to-validation flow | Global policy ownership and generic single-task execution ownership |
| `control-knowledge-explorer` | Knowledge exploration and evidence-gap mapping | Method implementation and final validation claims |
| `eda-idea-debate-lab` | Brainstorming and adversarial idea refinement | Experiment execution and production code changes |
| `eda-hypothesis-experiment-designer` | Hypothesis-to-experiment design with pass/fail criteria | Running production implementation changes directly |
| `eda-method-implementer` | Method implementation with integration contract and validation handoff | Final promotion decision without validation evidence |
| `bspdn-goal-driver` | Staged optimization toward explicit PPA goals with milestone gating | One-shot final-goal claim without intermediate evidence |
| `eda-infra-maintainer` | Infrastructure maintenance/development workflow for KB/tool/skills stack | Domain experiment logic and physics/model conclusions |
| `eda-experiment-phenomenology-analyst` | Horizontal extraction and maintenance of `log -> result -> conclusion -> experience` evidence layers for experiment workflows | Final veto ownership, global routing ownership, or replacement of `control-postrun-retro` decision logic |
| `eda-script-pattern-curator` | Horizontal maintenance of reusable script-writing patterns, wrapper/runtime lessons, abstraction triggers, and script-level anti-patterns | Replacing tool catalog ownership, owning domain conclusions, or bypassing infra/tool governance |
| `eda-artifact-hygiene-maintainer` | KB/tool/log artifact cleanup, duplicate merge, stale archive/delete, and naming normalization | Governance policy ownership and domain conclusion changes |
| `eda-knowledge-gate-maintainer` | Gate hygiene utility and maintenance logging | Task planning, cross-skill routing decisions |
| Domain skills (`bscost-*`, `gt3-*`, `delay-*`, paper/pdf, slides) | Domain logic and artifacts | Repo-wide orchestration decisions |

## Consolidation Decision
1. Agent duties formerly duplicated in legacy entry shims and `workflow-scoped-execution` are moved here.
2. Skill-routing duties formerly duplicated across `AGENTS.md`, `workflow-scoped-execution`, and compatibility docs are consolidated into `workflow-router`.
3. `workflow-scoped-execution` remains the primary owner for one scoped execution workflow, not the universal owner for all workflows.
4. Legacy compatibility shim `eda-chief` has been removed from the active skill system.

## Change Policy
1. Prefer updating specialized domain skills before orchestration skills.
2. Update `workflow-scoped-execution` only for repeated execution-level gaps.
3. Update this `AGENTS.md` when governance/routing policy changes.
