# Artifact Hygiene Cleanup Scope Policy

## Scopes

### Knowledge Base

Applies to:
- `docs/knowledge_base/*.md`
- KB indexes and supporting metadata when they are regenerated as part of cleanup

Typical actions:
- merge duplicated notes,
- rename unclear titles,
- archive stale status notes that have a newer canonical replacement.

### Tool Registry

Applies to:
- `docs/tool_registry/*`
- tool metadata notes and registry summaries

Typical actions:
- merge duplicated tool descriptions,
- correct tool naming or lifecycle labels,
- archive superseded registry entries.

### Logs

Applies to:
- `slurm_logs/00_meta/*`
- `slurm_logs/90_debug_monitor/*`
- `slurm_logs/99_misc/*`
- maintained repo logs or summary logs that are meant for long-term consumption

Typical actions:
- merge repeated summary logs,
- prune stale generated summaries after keeping a canonical artifact,
- normalize names for easier lookup,
- archive runtime sidecars and debug-only subdirectories while keeping canonical summaries and manifests visible.

## Mixed Scope Rule

If the cleanup spans more than one scope, keep the report grouped by scope so decisions remain auditable.
