# Skill Selection And New Skill Decision

## Skill Selection

Once the workflow is chosen:
1. identify the single `workflow_owner_skill` first,
2. enumerate only workflow-local candidate skills under that owner,
3. select the smallest set that covers the next bounded step,
4. avoid invoking broad orchestrators when a specialist skill is enough,
5. keep execution routing separate from tool implementation,
6. do not wrap utility or theory workflows in `workflow-scoped-execution` unless a bounded governed execution stage is explicitly needed.

## New Skill Decision Rule

Recommend `create_new_skill` only if the work has:
1. clear boundary,
2. specialized logic or assets,
3. repeatability,
4. likely future reuse.

Recommend `reuse_existing` if:
1. the task is a one-off detail,
2. the logic cleanly fits an existing skill,
3. adding a new skill would only fragment the system.

Recommend `defer` if:
1. the boundary is still unclear,
2. the temporary workflow has not yet shown repeat value.

## Temporary Workflow Promotion Rule

Promote a temporary workflow into a known workflow only when:
1. it recurs,
2. its steps are stable enough to document,
3. its skill subset is distinct enough from existing workflows,
4. promotion improves routing clarity more than it adds complexity.
