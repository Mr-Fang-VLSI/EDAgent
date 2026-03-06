---
name: eda-preflight-reflect
description: Before each experiment, analyze latest route/STA evidence, reflect on method gaps, and output concrete improvement hypotheses and next-step A/B plan. Use when user asks to start new experiments or when model/flow conclusions may be unstable.
---

# EDA Preflight Reflect

Run this skill before submitting new experiment batches.

## Step 1: Evidence lock (no guess mode)
Collect latest artifacts first:
1. case-level summary TSV/MD (`*.case.tsv`, `*.summary.md`)
2. route evidence (`backside_reroute.rpt`, routed DEF layer occupancy)
3. timing delta evidence (WNS/TNS/violating paths)
4. internet/primary-source references for current assumptions (routing policy, CTS/PDN layer practice, etc.)

If evidence is missing, mark `insufficient_evidence` and stop optimization claims.

## Step 2: Reflection checklist
Evaluate these checks explicitly:
1. `backside_presence`: Are there real backside nets in routed geometry?
2. `long_net_capture`: Is backside mostly capturing long nets above crossover threshold?
3. `timing_consistency`: Does increased backside usage improve or at least not hurt timing?
4. `capacity_pressure`: Are nTSV/backside regions overused (pressure likely distorting routing)?
5. `policy_vs_model`: Is behavior likely route-policy dominated rather than model-driven?

Use `references/checklist.md` and output pass/fail per item.

## Step 3: Produce one preflight reflection artifact
Generate one markdown before any new run:
- root cause ranking (top 3)
- one-line hypothesis per root cause
- one minimal A/B/C plan for next run
- explicit acceptance criteria

Recommended helper script:
```bash
python3 scripts/debug/pre_experiment_reflection.py --case-tsv <case.tsv> --out-prefix <out_prefix>
```

## Step 4: Model-gap decision
When short backside nets dominate, do NOT proceed with simple `min(front,back)` claims.
Switch to a judgment model path if either is true:
1. `short_share_in_back > 0.6`
2. `back_on_long_ratio < 0.5` while long nets exist

Judgment model should include at least:
1. timing criticality/slack budget
2. congestion-relief value
3. nTSV region capacity pressure
4. access/via risk

## Mandatory outputs
1. `preflight_reflection_*.md`
2. selected next-step plan (A/B/C)
3. explicit go/no-go for new experiment submission
