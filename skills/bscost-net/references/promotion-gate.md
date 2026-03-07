# BS Cost Net Promotion Gate

Promote the model into active optimization only if:
1. Gate-0 passes with fixed sign contract.
2. In key buckets, the model is not worse than HPWL.
3. Stability across the benchmark set is better than the HPWL baseline.

If not, keep the model in shadow mode and iterate parameters or structure.
