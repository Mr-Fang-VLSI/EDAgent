# Optimization and Gates

## Baseline and candidate
1. Baseline:
   - HPWL-only predictor (`hpwl_dbu`), trained on train fold only.
2. Candidate:
   - multi-feature theory-aware model (default: random forest regressor in current repo flow).

## Split strategy
1. Repeated K-Fold:
   - default `n_splits=5`, `n_repeats=2`
2. Same splits for baseline and candidate.

## Metrics
Per fold and aggregated:
1. Pearson(pred, target)
2. Spearman(pred, target)
3. Sign accuracy:
   - `sign(pred) == sign(target)`

## Gate thresholds (initial)
Per dataset:
1. mean delta Pearson > 0
2. mean delta Spearman >= 0
3. mean delta Sign > 0
4. fold win-rate:
   - Pearson >= 0.60
   - Spearman >= 0.55
   - Sign >= 0.60

Global:
1. all datasets pass per-dataset gates
2. no severe regression in any key bucket

## Promotion policy
1. PASS:
   - allow active-mode experiments with guarded scope.
2. FAIL:
   - remain shadow mode
   - adjust feature design or model class first.

