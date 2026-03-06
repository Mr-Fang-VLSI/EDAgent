---
name: eda-knowledge-gate-maintainer
description: Enforce experiment hygiene for this EDA repo. Utility skill for knowledge gate, tool reuse checks, and maintenance-log updates during scoped execution.
---

# EDA Knowledge Gate Maintainer

## Invocation Policy

1. Prefer invocation through `eda-loop`.
2. Direct invocation is for gate-hygiene repair/debug only.

Run this workflow before and after each substantive interaction.

## Step 1: Enter the repo and run gate

```bash
ROOT=/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00
cd "$ROOT"
bash scripts/common/knowledge_gate.sh --scope <scope_name> --task-brief <task_brief_md>
```

Use a task brief under `slurm_logs/04_delay_modeling/` or matching experiment folder.

## Step 2: Query existing tools before creating new scripts

```bash
python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>
```

Reuse existing scripts when possible. Only create new scripts when no suitable match exists.

## Step 3: Log interaction start/end maintenance

Append one row to:
- `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`

Minimum fields:
- `interaction_scope`
- `kb_used`
- `tool_query`
- `reused_or_new`
- `updates_done`
- `open_items`

Load `references/checklist.md` and follow the exact pre/post checklist.

## Step 4: Enforce hard gate behavior

Treat these as hard failures:
1. Gate command fails.
2. No tool-catalog query evidence for non-trivial work.
3. No maintenance-log update after file/script/job changes.
