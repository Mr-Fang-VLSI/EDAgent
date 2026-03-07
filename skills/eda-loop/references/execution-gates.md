# EDA Loop Execution Gates

Use this file for concrete gate checks after `SKILL.md` has selected `eda-loop`.

## Core Gates

Before substantive execution:
- run `knowledge_gate.sh`,
- query `tool_catalog.py`,
- enforce tri-source evidence for non-trivial conclusions,
- run `infra_stack_guard.py` for infrastructure maintenance/development tasks.

## Testcase-backed DC / Innovus

Before submission, run `check_design_package.py --require-design-top-match` and block on FAIL.

## Route / CTS

Before submission, run `pdk_flow_preflight.py` and block on FAIL.

## Direct Slurm CPU Submission

Default to `scripts/common/sbatch_cpu_research.sh` unless the experiment explicitly requires a different resource class.

## CTS / Route Non-convergence

If the task is about CTS/route non-convergence:
- switch to root-cause mode,
- vary one control only,
- classify the dominant mechanism before launching rescue sweeps.
