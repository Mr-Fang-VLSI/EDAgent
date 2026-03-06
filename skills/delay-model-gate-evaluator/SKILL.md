---
name: delay-model-gate-evaluator
description: Execute delay-model validation gates against HPWL baselines. Use when evaluating model consistency, running Gate-0 contract checks, building Gate-1 bucketed scorecards, or deciding readiness for active optimization.
---

# Delay Model Gate Evaluator

Run these checks before promoting model changes into placement/CTS optimization.

## Gate-0: Contract and sign consistency

```bash
ROOT=/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00
cd "$ROOT"

python3 scripts/debug/check_delay_model_contract.py \
  --input-tsv <merged_or_unified_tsv> \
  --delta-sign back_minus_front \
  --min-sign-acc 0.60 \
  --out-prefix slurm_logs/04_delay_modeling/<tag>.contract
```

Use `--strict` for CI-style hard fail.

## Gate-1: Bucketed scorecard

```bash
python3 scripts/debug/bucketed_delay_model_scorecard.py \
  --input-tsv <merged_or_unified_tsv> \
  --delta-sign back_minus_front \
  --out-prefix slurm_logs/04_delay_modeling/<tag>.bucketed
```

## Promotion criteria
1. Gate-0 sign contract passes.
2. Key buckets (long + high fanout) are not worse than HPWL.
3. Scorecard results are archived with clear run tag and data source.

Load `references/metric_contract.md` before interpreting results.
