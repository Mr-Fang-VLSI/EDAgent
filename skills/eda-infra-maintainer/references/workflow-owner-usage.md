# Workflow Owner Usage

Use this reference when deciding whether `eda-infra-maintainer` should remain the direct workflow owner or delegate one substage.

## Default Rule

`eda-infra-maintainer` directly owns:
1. policy updates,
2. manifest and skill-system maintenance,
3. KB/tool-registry governance maintenance,
4. guard/audit-driven integrity repair.

## Delegate To `workflow-scoped-execution` Only When

Delegate one bounded stage to `workflow-scoped-execution` only if the infrastructure task includes governed execution such as:
1. submitting a validation run,
2. producing monitored execution artifacts for a repaired flow,
3. running a scoped execution contract after infra changes.

## Reporting Requirement

The closeout should state:
1. `eda_loop_role = not_used` for pure maintenance,
2. `eda_loop_role = delegated_stage` when one execution substage was required.
