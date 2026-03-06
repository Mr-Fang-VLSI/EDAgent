# Model Plan

## Tracks
1. Signal-net model (front vs backside).
2. Clock-net model (front vs backside, clock-specific assumptions).

## Common fields
1. `cost_front`
2. `cost_back`
3. `delta_cost = cost_back - cost_front`
4. `min_cost = min(cost_front, cost_back)`
5. `capacity_pressure_proxy` (or region-exact overflow when available)

## Target alignment
Use matched target delay fields with fixed sign contract:
1. `tau_front_ps`
2. `tau_back_ps`
3. `delta_tau_ps = tau_back_ps - tau_front_ps`

## Evaluation
1. Gate-0:
   - contract validity
   - sign accuracy threshold
2. Gate-1:
   - Pearson/Spearman/sign by bucket
   - key-bucket outcomes (long + high-fanout)
3. Stability:
   - per-design variance
   - cross-design variance
   - seed sensitivity
4. Capacity behavior:
   - high-pressure regions/bins should show positive cost uplift.

## Promotion rule
Only promote to active optimization when:
1. Gate-0 pass.
2. Key buckets are no worse than HPWL.
3. Cross-design stability beats HPWL baseline.
