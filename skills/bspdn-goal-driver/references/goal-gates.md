# BSPDN Goal Gates

## Gate A: 8% dynamic-power goal
Required:
1. `delta_power_pct <= -8.0`
2. `delta_area_pct <= 0.0`
3. `delta_wns_ns >= 0.0`
4. `delta_tns_ns >= 0.0`

## Incremental milestones
1. M1: `delta_power_pct <= -1.0` + non-worse area/timing.
2. M2: `delta_power_pct <= -3.0` + non-worse area/timing.
3. M3: `delta_power_pct <= -5.0` + non-worse area/timing.
4. M4: Gate A or Gate B final success.

## Gate B: frequency uplift goal
Required:
1. power/area non-worse,
2. period sweep shows frequency uplift `>=5%`,
3. same policy lock and valid baseline pairing.

## Evidence validity
1. execution-contract PASS,
2. no unresolved fatal log signatures,
3. route-level metrics not NA.

## Reporting trigger (slides)
1. Do not emit slides on every loop.
2. Emit PDF version-summary only when validated best version first reaches `>=2%` power reduction (non-worse area/timing), then at higher milestones, or on Goal-B success.
