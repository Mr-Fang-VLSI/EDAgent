# Preflight Reflection Checklist

## Inputs
1. Latest `*.case.tsv` and `*.summary.md`
2. Routed DEF and `backside_reroute.rpt`
3. Timing summaries (`postRoute.summary.gz`)

## Checks
1. Backside existence: routed DEF has BM/BPR segments for targeted mode.
2. Long-net capture: compute `back_on_long_ratio` and `long_share_in_back`.
3. Timing alignment: compare WNS/TNS deltas between front/back runs.
4. Pressure risk: identify whether high backside use correlates with worse timing/DRV.
5. Policy dominance: identify runs where reroute report says success but DEF occupancy is absent/minimal.

## Output structure
1. Observations (facts only)
2. Hypotheses (ranked)
3. Next-step A/B/C with acceptance metrics
4. Go/No-Go decision
