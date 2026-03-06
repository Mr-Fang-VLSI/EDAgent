# Workflow Catalog (Workflow-First Routing)

EDAgent uses workflow-first routing:
1. classify request into workflow class,
2. choose next skill only in that workflow's subset.

## Workflow Classes

## 1) bug_fix
- Goal: fix regressions quickly with minimal scope.
- Skill subset: `eda-loop`, `eda-method-implementer`, `eda-infra-maintainer`, `eda-retro`.

## 2) repo_analysis
- Goal: understand architecture, gaps, and risks.
- Skill subset: `eda-knowledge-explorer`, `eda-infra-maintainer`, `eda-loop`.

## 3) feature_add
- Goal: add one new capability with explicit validation.
- Skill subset: `eda-hypothesis-experiment-designer`, `eda-method-implementer`, `git-version-control`, `eda-infra-maintainer`.

## 4) refactor
- Goal: improve structure without changing intended behavior.
- Skill subset: `eda-infra-maintainer`, `eda-method-implementer`, `git-version-control`.

## 5) environment_debug
- Goal: unblock deployment/check failures.
- Skill subset: `eda-infra-maintainer`, `eda-loop`, `eda-stage-checkpoint-golden`.

## 6) eda_experiment_orchestration
- Goal: run governed EDA hypothesis loops.
- Skill subset: `eda-preflight-reflect`, `eda-theory-veto`, `eda-loop`, `eda-retro`, `bspdn-goal-driver`.

## 7) infra_evolution
- Goal: maintain/develop KB/tool/skill infra safely.
- Skill subset: `eda-infra-maintainer`, `eda-knowledge-gate-maintainer`, `git-version-control`.

## 8) reporting_slides
- Goal: produce human-friendly summaries and slide outputs.
- Skill subset: `eda-retro`, `academic-presentation-crafter`, `academic-slide-refiner`.

## State Machine
All workflows should follow:
1. `PLAN`
2. `EXECUTE`
3. `CHECK`
4. `RECOVER`
5. `COMMIT`

## Trigger Phrases
Deployment onboarding trigger:
- `开始部署EDAgent`
- `Start deploying EDAgent`
