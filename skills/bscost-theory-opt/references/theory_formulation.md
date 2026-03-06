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
3. Backside overhead block:
   - nTSV distance/proxy, stack-via proxy
4. Optional congestion block:
   - backside demand/capacity proxy

## 4) Regime-aware modeling
Use regime split if needed:
1. short/mid/long length buckets
2. low/high fanout buckets
3. near/far TSV buckets

Model should be evaluated per bucket before promotion.

