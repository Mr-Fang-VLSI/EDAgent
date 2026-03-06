# Agent Responsibilities and Skill Boundaries

## Purpose
This file is the top-level execution policy for this repository.
Agent-level responsibilities must live here, not inside individual skills.

## Workflow-First Routing Policy
Agent must not do global skill selection across the full skill set by default.
Instead, use two-step routing:
1. classify current request into one workflow class,
2. select next skill only inside that workflow's allowed skill subset.

### Workflow Classes
1. `bug_fix`: diagnose and fix regressions in scripts/policies.
2. `repo_analysis`: inspect status, summarize architecture, map risks/gaps.
3. `feature_add`: add a new capability with minimal-risk integration.
4. `refactor`: improve structure without changing intended behavior.
5. `environment_debug`: deployment/bootstrap/check failures.
6. `eda_experiment_orchestration`: hypothesis-driven EDA execution loops.
7. `infra_evolution`: knowledge/tool/skill stack maintenance or development.
8. `reporting_slides`: explain results as concise summaries/slides.

### Workflow -> Skill Subsets
1. `bug_fix`: `eda-loop`, `eda-method-implementer`, `eda-infra-maintainer`, `eda-retro`
2. `repo_analysis`: `eda-knowledge-explorer`, `eda-infra-maintainer`, `eda-loop`
3. `feature_add`: `eda-method-implementer`, `eda-hypothesis-experiment-designer`, `eda-infra-maintainer`, `git-version-control`
4. `refactor`: `eda-infra-maintainer`, `eda-method-implementer`, `git-version-control`
5. `environment_debug`: `eda-infra-maintainer`, `eda-loop`, `eda-stage-checkpoint-golden`
6. `eda_experiment_orchestration`: `eda-preflight-reflect`, `eda-theory-veto`, `eda-loop`, `eda-retro`, `bspdn-goal-driver`
7. `infra_evolution`: `eda-infra-maintainer`, `eda-knowledge-gate-maintainer`, `git-version-control`
8. `reporting_slides`: `eda-retro`, `academic-presentation-crafter`, `academic-slide-refiner`

## Responsibility Split (Anti-Bloat Contract)
To keep orchestration scalable, responsibilities are explicitly separated:
1. classification layer (agent): determine workflow class.
2. routing layer (agent): choose next skill from workflow subset only.
3. parameter layer (skill interface): fill skill-level inputs/constraints.
4. execution layer (skill/tool): run scripts/tools and produce artifacts.
5. recovery layer (workflow policy): retry/fallback/escalation rules.
6. evaluation layer (workflow + domain gate): decide pass/fail/next step.
7. memory layer (infra policy): persist knowledge/SOP updates when justified.

Agent should own only layers 1-2 and high-level 5/6 decisions.
Skill/tool implementations should own layer 3-4 details.
Infra governance should own layer 7.

## Agent Owns (Global)
1. Interpret user intent, constraints, and risk level.
2. Classify workflow class and select minimal skill sequence within workflow subset.
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

## Standard Agent Flow
1. Classify request into one workflow class.
2. Build a workflow-local skill shortlist (not global skill search).
3. Pick next skill and execute one bounded step with explicit artifacts.
4. Evaluate result and either continue workflow, recover, or stop.
5. Run retrospective/memory update only when evidence justifies persistent change.

## Workflow State Machine
Each workflow step should follow:
1. `PLAN`: identify next bounded action.
2. `EXECUTE`: run selected skill/tool path.
3. `CHECK`: validate artifacts/metrics against workflow gates.
4. `RECOVER`: fallback/retry/alternative branch when check fails.
5. `COMMIT`: update knowledge/SOP/version records when check passes.

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

Deployment trigger phrases (equivalent):
1. `开始部署EDAgent`
2. `Start deploying EDAgent`
When either phrase is provided, start the onboarding contract immediately.

## Pre-Submit Hard Gate
1. Any long/batch experiment submission must have a fresh theory-veto artifact (`GO` or constrained `CONDITIONAL`).
2. `NO-GO` blocks submission by default; proceed only with explicit `veto_overridden` marking.

## Full Research Chain Flow
For end-to-end research requests, route by stages:
1. `eda-knowledge-explorer` (knowledge and evidence gap map),
2. `eda-paper-fetch` + `eda-pdf-local-summary` (literature queue and local parsing),
3. `eda-idea-debate-lab` (brainstorm + pro/con debate),
4. `eda-hypothesis-experiment-designer` (falsifiable experiment matrix),
5. `eda-method-implementer` (implementation and validation handoff),
6. `git-version-control` (multi-version checkpoints/integration),
7. `eda-loop` + validation stack (execution and decision),
8. `eda-retro` (post-run recursive decision).
For explicit long-horizon PPA goals, use `bspdn-goal-driver` to enforce staged milestone gates.

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

## Skill Boundary Table
| Skill | Owns | Does Not Own |
|---|---|---|
| `eda-loop` | Scoped execution orchestration (gate/tool query, routing, artifact validation) | Global entry policy, recursion governance, global self-update policy |
| `eda-chief` | Legacy compatibility dispatch for historical calls | Primary agent role and top-level governance |
| `eda-research-chain` | End-to-end research chain orchestration for idea-to-validation workflow | Global policy ownership |
| `eda-knowledge-explorer` | Knowledge exploration and evidence-gap mapping | Method implementation and final validation claims |
| `eda-idea-debate-lab` | Brainstorming and adversarial idea refinement | Experiment execution and production code changes |
| `eda-hypothesis-experiment-designer` | Hypothesis-to-experiment design with pass/fail criteria | Running production implementation changes directly |
| `eda-method-implementer` | Method implementation with integration contract and validation handoff | Final promotion decision without validation evidence |
| `bspdn-goal-driver` | Staged optimization toward explicit PPA goals with milestone gating | One-shot final-goal claim without intermediate evidence |
| `eda-infra-maintainer` | Infrastructure maintenance/development workflow for KB/tool/skills stack | Domain experiment logic and physics/model conclusions |
| `eda-knowledge-gate-maintainer` | Gate hygiene utility and maintenance logging | Task planning, cross-skill routing decisions |
| Domain skills (`bscost-*`, `gt3-*`, `delay-*`, paper/pdf, slides) | Domain logic and artifacts | Repo-wide orchestration decisions |

## Consolidation Decision
1. Agent duties formerly duplicated in `eda-chief` and `eda-loop` are moved here.
2. `eda-loop` remains the primary execution orchestrator skill.
3. `eda-chief` is retained as a compatibility shim for legacy prompts/workflows.

## Change Policy
1. Prefer updating specialized domain skills before orchestration skills.
2. Update `eda-loop` only for repeated execution-level gaps.
3. Update this `agent.md` when governance/routing policy changes.
