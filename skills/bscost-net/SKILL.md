---
name: bscost-net
description: Plan and execute internet-assisted backside net cost modeling for signal and clock nets, then evaluate stability and correlation against HPWL baselines across multiple designs. Use when users ask to improve/validate backside cost models, choose benchmark designs, compare model vs HPWL, or prepare publishable model-evaluation evidence.
---

# BS Cost Net

Use this skill to move model work from single-design intuition to reproducible, multi-design evidence.

## Step 1: Scope and objective lock
Define objective before tuning:
1. `Primary`: model is more stable than HPWL across designs/seeds.
2. `Secondary`: model improves correlation/sign behavior in key buckets (long/high-fanout clock-like nets).
3. `No-claim`: do not claim superiority from one design only.
4. Run preflight reflection first (`eda-preflight-reflect`) and capture current failure shape before designing next batch.

## Step 2: Internet-backed benchmark selection
Use network research with primary sources only:
1. Confirm candidate open-source CPU/accelerator repos and status.
2. Build benchmark set beyond systolic-array-only.
3. Record selected commit/release identifiers in experiment notes.

Minimum baseline set:
1. `systolic_array_*` (continuity with existing results)
2. `rocket-chip` class SoC design
3. `gemmini` class accelerator design

Load:
- `references/benchmark_candidates.md`
- `references/web_research_protocol.md`

## Step 3: Model construction plan
Build two model tracks:
1. Backside signal-net cost model.
2. Backside clock-net cost model.

For theory-grounded fitting and promotion gates, pair with:
1. `bscost-theory-opt`

For both tracks, keep output fields aligned:
1. `cost_front`, `cost_back`, `delta_cost`, `min_cost`
2. target delay fields with fixed sign contract
3. bucket tags (length, fanout, TSV-proxy)

Load:
- `references/model_plan.md`

## Step 4: Evaluation protocol (HPWL baseline required)
Always report model and HPWL side-by-side:
1. Contract check (Gate-0): sign convention + sign accuracy.
2. Bucketed scorecard (Gate-1): Pearson/Spearman/sign by regime.
3. Stability panel:
   - per-design and cross-design variance,
   - seed sensitivity,
   - pass-rate under fixed gate thresholds.

Use existing scripts first:
1. `scripts/debug/check_delay_model_contract.py`
2. `scripts/debug/bucketed_delay_model_scorecard.py`

## Step 5: Decision gate for promotion
Promote model into active optimization only if:
1. Gate-0 passes with fixed sign contract.
2. In key buckets, model is not worse than HPWL.
3. Stability across benchmark set is better than HPWL baseline.

If not, keep model in shadow mode and iterate parameters/structure.

## Mandatory artifacts
1. `contract.md/tsv` and `bucketed.md/tsv`
2. design list + source links + commits
3. one summary stating whether model is stably better than HPWL
