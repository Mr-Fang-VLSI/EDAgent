# Background Knowledge Links

This skill should stay coupled to the current BSPDN physical-contract knowledge, not to one-off intuition.

## Primary KB anchors

1. `docs/knowledge_base/107_BSPDN_TOPOLOGY_AND_BENEFIT_VALIDATION_PROGRAM_20260307.md`
- defines Gate A topology validity as the first mechanism gate

2. `docs/knowledge_base/20_LAYER_POLICY_CTS_PDN_BACKSIDE.md`
- current role split:
  - `BPR = PDN only`
  - `clock = M4+`
  - `backside signal = BM2/BM1 only`

3. `docs/knowledge_base/30_BACKSIDE_VIA_CONNECTIVITY_CHECKLIST.md`
- via/connectivity checklist for `BM1/BM2/nTSV`

4. `docs/knowledge_base/95_PROBLEM_LANDSCAPE.md`
- strongest linked problem nodes:
  - `P2 Backside Resource Allocation`
  - `P5 Via/TSV & Interconnect Constraints`

5. `docs/knowledge_base/96_METHOD_LANDSCAPE.md`
- strongest linked method families:
  - `M3 Backside Cost/Predictor Modeling`
  - `M4 Constraint-Guided Optimization`
  - `M5 A/B + Causal Validation`

## Current working knowledge summary

Current planning defaults are:
1. `BPR` should be treated as PDN-reserved unless disproved
2. backside signal should be interpreted through `BM2/BM1`
3. the signal-entry path is currently hypothesized as `BM2 -> BM1 -> M0 -> M1`
4. the power-entry path is currently hypothesized as `nTSV -> BPR`

These are not paper-grade truths yet.
This skill exists to determine which of them survive local collateral inspection and micro-test evidence.

## Paper-side intent to keep in mind

The dominant BSPDN narrative in the current local evidence base is:
1. power and signal should be attributable as separate resource roles
2. backside signal routing should not be justified by silently borrowing PDN-only resources
3. local PDK assumptions must not drift away from paper intent without being explicitly documented

## Newly added local papers worth reusing

1. `docs/papers/summaries/GOALPlace_Begin_with_the_End_in_Mind.summary.md`
- useful for the "begin with end-of-flow contract" mindset when deciding whether a local physical contract is realistic enough to optimize against

2. `docs/papers/summaries/DREAM-GAN_Advancing_DREAMPlace_towards_Commercial-Quality_using_Generative_Adversarial_Learning.summary.md`
- useful as a reminder that placement-stage signals are only trustworthy if they survive downstream flow

3. `docs/papers/summaries/Critical_Path_Aware_Timing_Driven_Global_Placement_for_Large-Scale_Heterogeneous_FPGAs.summary.md`
- useful for path-aware timing context when deciding whether a hypothesized backside signal path is likely to matter
