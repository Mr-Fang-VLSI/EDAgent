---
name: bspdn-goal-driver
description: Drive BSPDN objective optimization toward target outcomes (about 8% dynamic-power reduction without area/timing regression, or 5%+ frequency uplift with non-worse power/area) using gated experiments and evidence tracking.
---

# BSPDN Goal Driver

## When to use

Use this skill when the user asks to push objective/performance toward explicit PPA goals, not just run exploratory experiments.

## Goal contract

Target A:
- dynamic power reduction about `8%`,
- area/timing non-worse (`delta_area<=0`, `delta_wns>=0`, `delta_tns>=0`).

Target B:
- power/area non-worse,
- frequency uplift `>=5%` validated by period-sweep evidence.

## Milestone policy (incremental, mandatory)

Do not pursue one-shot final target. Use staged gates:
1. M0: evidence-valid baseline and repeatable A/B flow (`execution-contract PASS`).
2. M1: `power <= -1%` with non-worse area/timing.
3. M2: `power <= -3%` with non-worse area/timing.
4. M3: `power <= -5%` with non-worse area/timing.
5. M4: final target A (`~ -8%`) or target B (`>=5%` frequency uplift with non-worse power/area).

Promotion to next milestone requires current milestone PASS + retrospective note.

## Workflow

1. Build/update goal tracker:

```bash
python3 scripts/debug/track_bspdn_goal_progress.py --campaign-md <ppa_md> --out-prefix <prefix>
```

2. Select testcase tier:
- Tier-1: high backside-usage potential with route feasibility,
- Tier-2: mechanism-isolation testcase for fast iteration.

3. Run pre-submit checks:
- `eda-preflight-reflect`
- route smoke (`smoke_targeted_backside_route_toycase.sh`) for targeted net lists
- execution policy lock (`vanilla_replace` primary baseline)

4. Execute A/B campaign with strict gates:
- shared baseline and route policy,
- explicit net-selection policy/version tag,
- collect route PPA and execution-contract artifacts.

5. Decision:
- `GO` only when current milestone gate is satisfied with valid artifacts,
- otherwise update hypotheses and next-step campaign.

## Outputs

1. `bspdn_goal_progress.summary.md`
2. `bspdn_goal_progress.detail.tsv`
3. campaign plan (`goal_campaign_plan.md`)
4. evidence-backed milestone decision note (`M0/M1/.../M4`).

## Reporting policy (user-facing)

1. Do not generate slides for every process stage.
2. Generate a PDF version-summary only when a new validated version reaches a reporting milestone:
   - first reach `>=2%` power reduction with non-worse area/timing,
   - then each higher validated step (for example `>=3%`, `>=5%`, final target),
   - or Goal-B (`>=5%` frequency uplift with non-worse power/area).
3. Each version-summary slide deck must include method delta, key conclusions, core PPA table, and next-step plan.

## Hard rules

1. No promotion claim without execution-contract PASS.
2. Goal-B frequency claim must come from period sweep, not WNS proxy alone.
3. Record exact selector/route-hint config for each compared run.
