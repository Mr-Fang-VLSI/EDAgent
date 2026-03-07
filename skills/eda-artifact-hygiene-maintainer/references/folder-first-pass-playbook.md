# Folder First-Pass Cleanup Playbook

Use this playbook for a first exploratory cleanup across multiple folders.

## Goal

Turn one exploratory pass into:
1. a safe archive/rename pass on high-confidence noise,
2. a per-folder keep/archive/rename policy,
3. a reusable SOP for later hygiene runs.

## Directory Triage Order

1. Start with log-heavy folders where generated noise dominates:
- `slurm_logs/90_debug_monitor/`
- `slurm_logs/99_misc/`
- repo root runtime droppings if any reappear
2. Review curated knowledge folders without destructive churn:
- `docs/knowledge_base/`
- `docs/tool_registry/`
3. Treat source-bearing folders as review-only unless the task explicitly expands scope:
- `skills/`
- `scripts/`
- `designs/`

## First-Pass Actions By Folder Type

### Debug Or Scratch Log Folders

Examples:
- `slurm_logs/90_debug_monitor/`

Default first-pass action:
1. keep curated `.md` and primary `.tsv`,
2. archive `.out`, `.err`, `.log`, `.pid`, `.html`, and transient debug subdirectories,
3. keep unusual reproducer collateral (`.tcl`, `.def`, `.v`) in place unless there is a clearly better archive rule.

### Mixed Historical Log Folders

Examples:
- `slurm_logs/99_misc/`

Default first-pass action:
1. keep summaries and canonical manifests,
2. archive monitor sidecars such as `.monitor.log`, `.monitor.pid`, `.monitor.history.tsv`,
3. archive obvious duplicates such as `.dup1` and `.dup2`,
4. normalize filenames only when the current name is actively misleading.

### Canonical Knowledge Folders

Examples:
- `docs/knowledge_base/`
- `docs/tool_registry/`

Default first-pass action:
1. do not merge or delete on filename similarity alone,
2. review for naming drift and obsolete placeholders,
3. defer content merge until canonical ownership is clear.

## Required Outputs

For every first-pass run, produce:
1. one report that groups findings by folder,
2. one archive/delete/rename TSV,
3. one maintenance-log entry,
4. one follow-up list of folders that still need deeper review.
