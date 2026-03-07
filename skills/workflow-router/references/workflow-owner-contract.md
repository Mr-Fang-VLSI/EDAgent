# Workflow Owner Contract

This reference defines who owns a workflow after routing.

## Control-Plane Layers

1. Agent:
- owns user communication and repo-wide governance,
- does not own reusable workflow selection details.

2. `workflow-router`:
- classifies the request,
- selects one `workflow_owner_skill`,
- defines the allowed downstream skill subset.

3. `workflow_owner_skill`:
- owns orchestration inside that workflow,
- may delegate bounded stages to specialist or utility skills,
- may delegate a governed execution stage to `eda-loop` only when execution wrapping is actually needed.

## Workflow Owner Rule

Every non-trivial task should have exactly one active workflow owner.

Examples:
1. single scoped experiment or debug execution -> `eda-loop`
2. end-to-end research chain -> `eda-research-chain`
3. infrastructure maintenance workflow -> `eda-infra-maintainer`
4. artifact cleanup workflow -> `eda-artifact-hygiene-maintainer`
5. pure theory judgment or specialist analysis -> the specialist skill itself

## `eda-loop` Rule

`eda-loop` is:
1. the owner for one scoped execution workflow,
2. a delegated execution subworkflow inside larger workflows when governed execution is needed,
3. not the universal wrapper for utility, theory, or research-chain tasks.

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
