# Gate Run And Tool Query

Use this reference when running the repo hygiene gate and tool reuse query.

## Gate Command

```bash
ROOT=/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00
cd "$ROOT"
bash scripts/common/knowledge_gate.sh --scope <scope_name> --task-brief <task_brief_md>
```

Use a task brief under the relevant `slurm_logs/` subtree or matching experiment folder.

## Tool Query

```bash
python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>
```

Reuse existing scripts when the fit is adequate. Only create new scripts when no suitable match exists.
