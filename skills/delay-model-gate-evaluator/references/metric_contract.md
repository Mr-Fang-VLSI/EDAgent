# Metric Contract

## Required derived fields
- `delta_tau_ps = tau_back - tau_front`
- `delta_cost = cost_back - cost_front`
- `min_cost = min(cost_front, cost_back)`

## Required reports
- Pearson
- Spearman
- sign_accuracy (`sign(delta_cost)` vs `sign(delta_tau_ps)`)

## Common failure modes
1. Sign convention mismatch (`front-back` vs `back-front`).
2. Comparing `min_cost` to a delta target without explicit contract.
3. Mixed net populations across model and target TSVs.

## Release discipline
- Treat scorecards as versioned artifacts under `slurm_logs/04_delay_modeling/`.
- Do not claim model superiority from internal-only synthetic metrics.
