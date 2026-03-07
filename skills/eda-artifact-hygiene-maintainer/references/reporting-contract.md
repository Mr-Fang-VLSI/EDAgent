# Artifact Hygiene Reporting Contract

Every hygiene run must leave behind traceable artifacts.

## Required Report Fields

1. timestamp
2. skill name
3. target scope
4. touched folders
5. actions taken
6. counts of archived, deleted, renamed, and review-only items
7. follow-up folders and unresolved risks

## Required Traceability Files

1. one markdown report under `slurm_logs/00_meta/`
2. one TSV listing each archive, delete, or rename action
3. one row appended to `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`

## Reporting Rule

If the run spans multiple folders, report them separately so later maintenance can reuse the folder-level policy without re-auditing the whole repo.
