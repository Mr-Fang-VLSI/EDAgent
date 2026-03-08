# BSPDN Campaign Workflow

## Build Or Update Goal Tracker

```bash
python3 scripts/debug/track_bspdn_goal_progress.py --campaign-md <ppa_md> --out-prefix <prefix>
```

## Select Testcase Tier

- Tier-1: high backside-usage potential with route feasibility,
- Tier-2: mechanism-isolation testcase for fast iteration.

## Pre-submit Checks

- `control-preflight-reflect`
- route smoke (`smoke_targeted_backside_route_toycase.sh`) for targeted net lists
- execution policy lock (`vanilla_replace` primary baseline)

## Execute A/B Campaign

- shared baseline and route policy,
- explicit net-selection policy and version tag,
- collect route PPA and execution-contract artifacts.

## Decision

- `GO` only when the current milestone gate is satisfied with valid artifacts,
- otherwise update hypotheses and next-step campaign.
