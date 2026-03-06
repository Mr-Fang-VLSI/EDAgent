---
name: bscost-theory-opt
description: Build and validate theory-grounded optimization models for backside front-vs-back net cost (signal and clock), with strict metric contracts and stability gates against HPWL baselines. Use when users request principled model fitting, crossover reasoning, or promotion decisions from shadow mode to active optimization.
---

# BS Cost Theory Opt

Use this skill when the task is to move from heuristic cost terms to a validated optimization model that can be promoted only after passing gates.

## Step 1: Lock metric contract before fitting
1. Use signed target:
   - `delta_tau_ps = tau_back_ps - tau_front_ps`
2. Use signed model output:
   - `delta_cost = cost_back - cost_front`
3. Keep compatibility fields:
   - `cost_front`, `cost_back`, `min_cost`
4. Gate-0 contract checks are mandatory before any optimization claim.

## Step 2: Theory-grounded feature setup
Build from physically meaningful inputs first:
1. Geometry:
   - pin-based HPWL and bbox features
2. Front/back timing proxy:
   - PDK timing proxy, via proxy, fanout/load terms
3. Backside overhead:
   - nTSV/stack-via related terms (or best available proxy)

Use shared feature names across signal and clock tracks where possible.

Load:
- `references/theory_formulation.md`

## Step 3: Optimization procedure
1. Compare against HPWL baseline with identical split strategy.
2. Use repeated cross-validation (default 5x2).
3. Report per-fold and per-dataset metrics:
   - Pearson
   - Spearman
   - sign accuracy
4. Use same train/test partitions for baseline and candidate model.

Load:
- `references/optimization_and_gates.md`

## Step 4: Promotion gates (stable > HPWL)
Model can be promoted only if:
1. Gate-0 pass:
   - contract valid
   - sign convention fixed
2. Gate-1 (delay consistency) pass on all target datasets:
   - `delta_pearson > 0`
   - `delta_spearman >= 0`
   - `delta_sign > 0`
   - fold win-rate thresholds satisfied
3. Gate-2 (absolute consistency floor) pass:
   - candidate Pearson/Spearman/sign must exceed configured minimum floors
4. Gate-3 (nTSV capacity behavior) pass:
   - high-pressure bins/regions must receive positive cost uplift
   - if coordinate-level region data is unavailable, use an explicit pressure proxy and mark as `proxy mode`
5. Stability pass:
   - no single dataset collapses below baseline in key metrics.

If any gate fails, keep shadow mode and iterate model/feature design.

## Step 5: Internet-backed benchmark expansion
When moving beyond current datasets:
1. Validate benchmark provenance from primary sources.
2. Record repo links + commit/branch in summary artifact.
3. Include CPU + accelerator classes (not only systolic arrays).

Load:
- `references/internet_benchmark_notes.md`

## Mandatory artifacts
1. `*.dataset.tsv` (dataset-level scorecard)
2. `*.per_fold.tsv` (fold-level evidence)
3. `*.summary.md` with final PASS/FAIL and open risks
4. include gate mode flag: `region_exact` vs `proxy_mode`
