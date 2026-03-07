# Workflow Owner Usage

Use this reference when deciding whether `git-version-control` is the direct workflow owner or a delegated substage.

## Default Rule

`git-version-control` directly owns:
1. standalone snapshot/checkpoint requests,
2. version comparison and rollback-point preparation,
3. version-log maintenance tied to git history.

## Delegated Context

Treat versioning as a delegated substage when:
1. `eda-research-chain` reaches a versioned development milestone,
2. `eda-method-implementer` requests a checkpoint after a bounded implementation step,
3. an execution workflow explicitly needs a reproducible rollback point after completion.

## `eda-loop` Rule

`eda-loop` is normally `not_used` for versioning.
Use `eda-loop` only if the parent workflow has a governed execution stage and versioning is the closeout of that delegated stage.

## Reporting Requirement

The closeout should state:
1. whether `git-version-control` was the direct workflow owner,
2. or whether it was a delegated versioning stage under another workflow owner.
