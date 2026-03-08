# Update Mechanism

Refresh this skill when:

## Refresh triggers

1. a new project-preferred conda env is introduced,
2. the repo changes its default Python or package-management strategy,
3. multiple workflows start depending on a new package family,
4. shell initialization or PATH precedence changes enough to alter the effective env source,
5. repeated failures show that explicit `conda run -n ...` contracts are still missing or inconsistent.

## What to update

1. refresh `background-knowledge-links.md`
2. refresh the environment workflow note in `docs/knowledge_base/114_CONDA_PROJECT_ENVIRONMENT_MANAGEMENT_WORKFLOW_20260307.md`
3. update manifest/tool references if the preferred snapshot/report script changes
4. add or revise skill-adoption tracking if the skill becomes a repeated helper in active workflows

## Promotion rule

Do not expand this skill into a workflow owner.
Keep it as an auxiliary utility skill unless project environment management itself becomes a standalone recurring workflow with multiple governed stages.
