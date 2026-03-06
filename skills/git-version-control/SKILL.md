---
name: git-version-control
description: Use git to version-control local research/EDA iterations with reproducible checkpoints, clear commit/tag structure, and explicit per-version differentiation records. Use when users ask to create baselines, compare versions, snapshot experiment states, prepare rollback points, or document each version's characteristics and distinguishing deltas.
---

# Git Version Control

## Overview

Create a repeatable git-based versioning workflow for experiments and code changes.
Record each version with both git artifacts (commit/tag) and human-readable differentiators in a version log.

## Workflow

1. Inspect repository state before versioning.
2. Define version scope and naming.
3. Create commit and optional tag.
4. Update version log with characteristics and distinguishing points.
5. Validate traceability (`git show`, `git log`, file references).

## Step 1: Inspect State

Run:
- `git status --short`
- `git branch --show-current`
- `git log --oneline -n 5`

If working tree contains unrelated dirty files, avoid touching them.
Never use destructive reset/checkout unless user explicitly requests.

## Step 2: Define Version Identity

Prefer one clear version token:
- `v<major>.<minor>.<patch>` for stable releases
- `<topic>_YYYYMMDD_HHMM` for experiment snapshots

Recommended commit title format:
- `<scope>: <version-token> <short-change-intent>`
- Example: `delay-model: v0.3.1 enable criticality feed in scorer`

## Step 3: Commit and Tag

Typical sequence:
```bash
git add <changed-files>
git commit -m "<scope>: <version-token> <short-change-intent>"
git tag -a "<version-token>" -m "<summary>"   # optional but recommended for checkpoints
```

If user wants comparison-only checkpoint without tagging, skip tag and record commit hash in log.

## Step 4: Record Version Characteristics and Distinguishing Points

Maintain one log file for the active project/topic, for example:
- `docs/versioning/<topic>.version_log.md`

Use template and field definitions from:
- `references/version-log-template.md`

Mandatory fields per version entry:
- version token / tag / commit hash
- baseline reference (which previous version it compares to)
- `characteristics` (本版本特点)
- `distinguishing_points` (和基线的区分点)
- changed files and validation evidence

## Step 5: Validate Traceability

After each version entry, verify:
- `git show --stat <commit-or-tag>`
- `git diff --name-only <baseline>...<current>`
- log file contains the same commit hash/tag and accurate delta summary

## Command Playbook

- latest version list: `git tag --list --sort=-creatordate`
- compare two versions: `git diff --stat <v_old>...<v_new>`
- inspect one version: `git show --name-status <tag-or-hash>`
- recover file from version: `git checkout <tag-or-hash> -- <path>` (non-destructive to history)

## Resources (optional)
- `references/version-log-template.md`: canonical template for per-version feature/delta logging.
