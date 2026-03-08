# Workflow Owner Usage

Use this reference when deciding whether `eda-artifact-hygiene-maintainer` should directly own the cleanup workflow or operate as a delegated substage.

## Default Rule

`eda-artifact-hygiene-maintainer` directly owns:
1. standalone cleanup requests,
2. duplicate merge and archive decisions,
3. naming normalization passes,
4. folder-by-folder hygiene exploration.

## Delegate Context

Treat cleanup as a delegated substage only when:
1. a larger maintenance workflow explicitly requests a cleanup phase,
2. an execution or research workflow needs post-run artifact normalization,
3. the parent workflow still owns the overall objective while hygiene is only one bounded step.

## `workflow-scoped-execution` Rule

`workflow-scoped-execution` is normally `not_used` for cleanup.
Use `workflow-scoped-execution` only if a larger execution workflow delegates a governed stage that happens to include cleanup, not as the default owner for hygiene work.

## Reporting Requirement

The cleanup report should state whether the cleanup was:
1. a direct owner workflow, or
2. a delegated cleanup stage under another workflow owner.
