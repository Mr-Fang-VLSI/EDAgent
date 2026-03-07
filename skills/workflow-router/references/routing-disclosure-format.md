# Routing Disclosure Format

Use this reference when the routing result must be surfaced to the user.

## Minimum Disclosure

State these fields explicitly:
1. `Detected workflow: <workflow_name>`
2. `Workflow owner: <workflow_owner_skill>`
3. `Skills used: <skill list>`
4. `New workflow decision: <reuse_existing | create_new_workflow | no_new_workflow>`

## Usage Rule

1. Use this disclosure whenever workflow or skill selection is non-trivial.
2. If routing was obvious and `workflow-router` was not explicitly invoked, still disclose the effective workflow and selected skills before substantive work.
3. Keep the disclosure short; it is a control-plane statement, not a long explanation.
