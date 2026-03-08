# Theory Formulation (Signal + Clock)

## 1) Objective framing
For each net `n`, define:
- `cost_front(n)`
- `cost_back(n)`
- `delta_cost(n) = cost_back(n) - cost_front(n)`

Target:
- `delta_tau_ps(n) = tau_back_ps(n) - tau_front_ps(n)`

The optimization goal is not raw curve fitting only; it is stable predictive ordering/sign vs `delta_tau_ps`.

## 2) Soft-min compatibility
If placement optimizer still consumes min-like objective:
- `min_cost = softmin(cost_front, cost_back; tau)`
- keep `delta_cost` as validation target for sign and tradeoff analysis.

## 3) Recommended feature blocks
1. Geometry block:
   - pin-HPWL, bbox width/height, route-length proxy
2. Electrical block:
   - PDK timing proxy, load/fanout terms
   - extracted front/back total cap
   - extracted front/back max-R and max-tau
3. Backside overhead block:
   - nTSV distance/proxy, stack-via proxy
   - explicit `VBM2BM1`, `VBM1M0`, `V0_0` access-via counts
   - explicit `BM2/BM1/M0` segment occupancy
4. Optional congestion block:
   - backside demand/capacity proxy
5. Structural block:
   - sink count / fanout
   - reachable fraction
   - branch/access detour indicators when available

## 3.1) RC-aware upgrade requirement
Promotion past crossover-only modeling now requires one unified feature table with:
- `fanout_n` kept explicit, not hidden in `C_load`
- per-net extracted `front/back` RC terms
- access/via penalties from the actual routed or patched path
- physical realization markers (`used_bm`, `used_m0_only`)

If a candidate model lacks these fields, it remains a proxy model and must not
be described as an RC-aware timing predictor.

## 4) Regime-aware modeling
Use regime split if needed:
1. short/mid/long length buckets
2. low/high fanout buckets
3. near/far TSV buckets

Model should be evaluated per bucket before promotion.

## 5) Promotion guard
Do not interpret geometric backside occupancy as electrical benefit unless the
same net also has extracted front-vs-back RC/tau comparison.
