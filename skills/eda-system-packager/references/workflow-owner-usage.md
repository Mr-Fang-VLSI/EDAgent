# Workflow Owner Usage

Use this reference when deciding whether `eda-system-packager` is the direct workflow owner or a delegated substage.

## Default Rule

`eda-system-packager` directly owns:
1. standalone bundle creation,
2. export refresh tasks,
3. repository-ready packaging preparation.

## Delegated Context

Treat packaging as a delegated substage when:
1. `eda-infra-maintainer` includes a release/export phase,
2. a larger maintenance workflow requires a portable handoff artifact,
3. packaging is only one bounded step under a broader infrastructure objective.

## `eda-loop` Rule

`eda-loop` is normally `not_used` for packaging.
Use it only if a parent workflow explicitly delegates one governed execution stage that must emit a package artifact.
