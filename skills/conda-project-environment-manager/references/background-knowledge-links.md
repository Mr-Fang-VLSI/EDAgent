# Background Knowledge Links

Use these sources when the repo needs explicit conda environment management rather than ad hoc shell debugging.

## Primary local sources

1. [AGENTS.md](/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00/AGENTS.md)
   - global governance and infrastructure stewardship rules
2. [112_PAPER_LEARNING_AND_EXPERT_REFRESH_FLOW_20260307.md](/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00/docs/knowledge_base/112_PAPER_LEARNING_AND_EXPERT_REFRESH_FLOW_20260307.md)
   - example of a workflow that benefits from explicit env control when PDF/summary tooling diverges from system Python
3. [114_CONDA_PROJECT_ENVIRONMENT_MANAGEMENT_WORKFLOW_20260307.md](/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00/docs/knowledge_base/114_CONDA_PROJECT_ENVIRONMENT_MANAGEMENT_WORKFLOW_20260307.md)
   - canonical env-management contract for this repo
4. [~/.bashrc](/home/grads/d/donghao/.bashrc)
   - current conda initialization and PATH precedence

## Current project environment topology

Current repo usage already shows multiple Python roots:
- system `python3.11`
- `~/miniconda3`
- `/mnt/research/Hu_Jiang/Students/Fang_Donghao/anaconda3`

This means shell PATH alone is not a trustworthy indicator of which environment a workflow is using.

## Current management baseline

The preferred baseline is:
1. discover available conda roots/envs with a scriptable snapshot,
2. choose one explicit env per tool family where non-system packages matter,
3. invoke scripts through `conda run -n <env> ...` when reproducibility matters,
4. keep environment decisions visible in artifacts rather than hidden in shell state.
