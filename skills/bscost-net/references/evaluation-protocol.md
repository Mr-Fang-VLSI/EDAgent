# BS Cost Net Evaluation Protocol

Always report model and HPWL side-by-side:
1. Contract check (Gate-0): sign convention and sign accuracy.
2. Bucketed scorecard (Gate-1): Pearson, Spearman, and sign by regime.
3. Stability panel:
- per-design and cross-design variance,
- seed sensitivity,
- pass-rate under fixed gate thresholds.

Use existing scripts first:
1. `scripts/debug/check_delay_model_contract.py`
2. `scripts/debug/bucketed_delay_model_scorecard.py`
