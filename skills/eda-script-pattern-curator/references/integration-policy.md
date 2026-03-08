# Integration Policy

## `eda-infra-maintainer`

Use when infra work discovers a script lesson that should outlive the immediate patch.

Expected behavior:
1. query existing tools first,
2. decide whether the lesson is a local fix or a reusable pattern,
3. persist reusable patterns in KB or skill references.

## `eda-method-implementer`

Use before adding a new helper or wrapper when similar logic may already exist.

## `workflow-scoped-execution`

Use after execution-side scripting incidents when the lesson should influence future batches.

## `eda-context-accessor`

Use to retrieve relevant script-pattern notes before creating new tooling.
