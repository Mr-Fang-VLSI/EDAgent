# Version Log Template (Git-Coupled)

Use one file per topic, for example `docs/versioning/<topic>.version_log.md`.

## Header

```md
# <topic> Version Log

- owner: <name/team>
- repository: <repo-path-or-name>
- purpose: <what this version line tracks>
```

## Entry Template

```md
## <version-token>
- date: <YYYY-MM-DD HH:MM TZ>
- tag: `<tag-or-NA>`
- commit: `<full-or-short-hash>`
- branch: `<branch-name>`
- baseline: `<previous-version-token-or-hash>`
- scope: <modules/experiments affected>

### Characteristics (特点)
1. <key characteristic 1>
2. <key characteristic 2>
3. <key characteristic 3>

### Distinguishing Points (区分点, vs baseline)
1. <delta 1: behavior/algorithm/flow>
2. <delta 2: config/parameter/policy>
3. <delta 3: artifact/result impact>

### Changed Files
1. `<abs-or-repo-relative-path-1>`
2. `<abs-or-repo-relative-path-2>`

### Validation Evidence
1. `git show --stat <commit-or-tag>` summary
2. `<result artifact path>`

### Risks / Follow-up
1. <open risk or unknown>
2. <next step>
```

## Minimum Quality Rules

1. `baseline` must be explicit for every entry.
2. `characteristics` must describe the version itself, not only outcome.
3. `distinguishing points` must be comparison statements against baseline.
4. `changed files` must match `git show --name-status`.
5. If there is no tag, commit hash is mandatory.
