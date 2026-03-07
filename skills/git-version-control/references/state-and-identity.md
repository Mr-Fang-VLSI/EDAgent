# Git Version State And Identity

## Inspect State

Run:
- `git status --short`
- `git branch --show-current`
- `git log --oneline -n 5`

If the working tree contains unrelated dirty files, avoid touching them.

## Define Version Identity

Prefer one clear version token:
- `v<major>.<minor>.<patch>` for stable releases,
- `<topic>_YYYYMMDD_HHMM` for experiment snapshots.

Recommended commit title format:
- `<scope>: <version-token> <short-change-intent>`
- Example: `delay-model: v0.3.1 enable criticality feed in scorer`
