# Workflow Owner Contract

This reference defines who owns a workflow after routing and how that differs from orchestration.

## Control-Plane Layers

1. Agent:
- owns user communication and repo-wide governance,
- does not own reusable workflow selection details.

2. `workflow-router`:
- classifies the request,
- selects one `workflow_owner_skill`,
- defines the allowed downstream skill subset,
- does not own execution semantics.

3. `workflow_owner_skill`:
- owns orchestration inside that workflow,
- may delegate bounded stages to specialist or utility skills,
- may delegate a governed execution stage to `workflow-scoped-execution` only when execution wrapping is actually needed.

4. `workflow-scoped-execution`:
- owns bounded governed execution orchestration,
- is the workflow owner only for one scoped execution workflow,
- is otherwise a delegated execution stage rather than a universal wrapper.

## Workflow Owner Rule

Every non-trivial task should have exactly one active workflow owner.

Examples:
1. single scoped experiment or debug execution -> `workflow-scoped-execution`
2. end-to-end research chain -> `workflow-research-chain`
3. infrastructure maintenance workflow -> `eda-infra-maintainer`
4. artifact cleanup workflow -> `eda-artifact-hygiene-maintainer`
5. pure theory judgment or specialist analysis -> the specialist skill itself

## `workflow-scoped-execution` Rule

`workflow-scoped-execution` is:
1. the owner for one scoped execution workflow,
2. a delegated execution subworkflow inside larger workflows when governed execution is needed,
3. not the universal wrapper for utility, theory, or research-chain tasks.

## Short Contract

Use this short sentence:

1. `workflow-router` picks the owner
2. the selected owner owns workflow semantics
3. `workflow-scoped-execution` owns only bounded execution orchestration

If a decision violates this sentence, the routing/orchestration split is probably wrong.

## Required Routing Output

Routing should explicitly produce:
1. `workflow_name`
2. `workflow_owner_skill`
3. `workflow_family`
4. `allowed_skill_subset`
5. `next_skill`
6. `eda_loop_role = owner | delegated_stage | not_used`

## Disclosure Rule

These routing outputs are not internal-only.
They should be reflected into the user-facing execution preamble in compact form so the user can see which workflow was recognized, which skill owns it, and whether a new workflow was required.
