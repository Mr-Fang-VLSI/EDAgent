# Git Commit Tag And Traceability

## Commit And Tag

Typical sequence:

```bash
git add <changed-files>
git commit -m "<scope>: <version-token> <short-change-intent>"
git tag -a "<version-token>" -m "<summary>"   # optional but recommended for checkpoints
```

If the user wants a comparison-only checkpoint without tagging, skip the tag and record the commit hash in the version log.

## Record Version Characteristics

Maintain one log file for the active project/topic, for example:
- `docs/versioning/<topic>.version_log.md`

Mandatory fields per version entry:
- version token, tag, or commit hash,
- baseline reference,
- `characteristics`,
- `distinguishing_points`,
- changed files and validation evidence.

## Validate Traceability

After each version entry, verify:
- `git show --stat <commit-or-tag>`
- `git diff --name-only <baseline>...<current>`
- the version log contains the same commit hash or tag and an accurate delta summary.

## Command Playbook

- latest version list: `git tag --list --sort=-creatordate`
- compare two versions: `git diff --stat <v_old>...<v_new>`
- inspect one version: `git show --name-status <tag-or-hash>`
- recover file from version: `git checkout <tag-or-hash> -- <path>` (non-destructive to history)
