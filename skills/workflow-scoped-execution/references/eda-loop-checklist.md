# EDA Loop Execution Checklist

Use this file only after `SKILL.md` has already determined that `workflow-scoped-execution` is the right execution skill.

## Bootstrap

1. Ensure the task brief exists and links the minimum required KB files.
2. Run:

```bash
bash scripts/common/knowledge_gate.sh --scope <scope_name> --task-brief <task_brief_md>
```

3. Query existing tools before adding scripts:

```bash
python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>
```

4. For infrastructure maintenance/development tasks, also run:

```bash
python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_<tag>
```

## Pre-submission gates

### Common

- Run `control-preflight-reflect` before any new experiment submission/comparison batch.
- Keep artifact paths explicit: `monitor.md`, `summary.md`, `manifest.tsv`, `execution_contract.md`.
- If a gate fails, fix the cause before proceeding.

### Testcase-backed DC / Innovus

Run and block on FAIL:

```bash
python3 scripts/common/check_design_package.py --design <design> --require-design-top-match --out-md <report.md>
```

### Route / CTS

Run and block on FAIL:

```bash
python3 scripts/debug/pdk_flow_preflight.py \
  --techlef <techlef> \
  --lef-dir <lef_dir> \
  --lib-dir <lib_dir> \
  --netlist <netlist> \
  --sdc <sdc> \
  --out-md <report.md>
```

### Direct Slurm submission

Use canonical CPU defaults unless the experiment explicitly requires a different resource class:

```bash
bash scripts/common/sbatch_cpu_research.sh ...
```

Defaults:
- partition: `cpu-research`
- qos: `olympus-cpu-research`
- account: `all`

## Root-cause mode

Use this branch when CTS/route behavior is unstable and repeated rescue sweeps would waste compute.

1. Freeze the current resume DEF and comparison baseline.
2. Vary one control only.
3. Classify the dominant mechanism as one of:
   - `placement_legality`
   - `pdk_mismatch`
   - `internal_tool_stage`
   - `mixed`
4. Record:
   - first appearance of `IMPCCOPT-2030`, `IMPSP-2020`, `IMPSP-2031`, `IMPSP-2042`
   - cumulative counts of `Orientation_Violation`, `DRC_Violation`, `Soft_Blockage_Violation`
5. Distinguish `entry-clean` from `stage-stable`.
6. Stop low-value branches once the dominant mechanism is identified.

## Monitoring and reporting

Immediately after submission, report in the same turn:
- `monitor.md`
- `manifest.tsv`
- job ids
- current stage
- ETA basis if ETA is provided

Do not treat submission as complete until monitoring visibility is available.

## Post-run closeout

1. Run execution-contract validation:

```bash
python3 scripts/debug/validate_execution_contract.py ...
```

2. Update:
- `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`
- `docs/knowledge_base/90_HYPOTHESIS_VALIDATION_LOG.md` when a hypothesis was tested

3. If optimization continues, ingest memory and propose constrained follow-ups:

```bash
python3 scripts/common/experiment_memory.py ...
python3 scripts/debug/propose_constrained_experiments.py ...
```

4. If the skill changed, validate it:

```bash
python3 /home/grads/d/donghao/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill_path>
```

## Comparison policy

- For algorithmic claims, the primary baseline must be `vanilla_replace`.
- Innovus is secondary realizability validation, not the primary algorithmic baseline.
- If only Innovus baseline exists, mark the algorithmic conclusion invalid and stop promotion.
