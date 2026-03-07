# Maintenance Log Writeback

Use this reference when recording the interaction into the maintenance log.

## Target

Append one row to:
- `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`

## Minimum Fields

1. `interaction_scope`
2. `kb_used`
3. `tool_query`
4. `reused_or_new`
5. `updates_done`
6. `open_items`

## Writeback Rule

Any interaction that changes files, scripts, jobs, or maintained reports must leave a corresponding log row.
