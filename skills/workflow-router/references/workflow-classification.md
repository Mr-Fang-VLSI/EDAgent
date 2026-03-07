# Workflow Classification

## Match Against Known Workflows

Try to match the task against the known workflow catalog first.

If a clean fit exists:
- mark `workflow_status = known`,
- assign one `workflow_owner_skill`,
- do not search globally across all skills,
- build the shortlist only from that workflow's allowed subset.

## Handle Unknown Workflows Explicitly

If no clean fit exists:
- mark `workflow_status = unknown`,
- create `workflow_name = temporary_<descriptive_name>`,
- assign one temporary `workflow_owner_skill`,
- state why known workflows are insufficient,
- choose the smallest safe temporary skill chain.

Do not silently squeeze unknown work into a nearby known workflow.
