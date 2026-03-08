# Background Knowledge Links

This skill should stay grounded in the current benefit-attribution narrative and fairness policy.

## Primary KB anchors

1. `docs/knowledge_base/107_BSPDN_TOPOLOGY_AND_BENEFIT_VALIDATION_PROGRAM_20260307.md`
- Gate D defines the canonical three-arm comparison and promotion rule

2. `docs/knowledge_base/20_LAYER_POLICY_CTS_PDN_BACKSIDE.md`
- fixes the current physical comparison contract:
  - `BPR = PDN only`
  - `clock = M4+`
  - `backside signal = BM2/BM1 only`

3. `docs/knowledge_base/84_REPLACE_COMPARISON_POLICY_20260304.md`
- reminds the system that comparison fairness must stay explicit

4. `docs/knowledge_base/95_PROBLEM_LANDSCAPE.md`
- strongest linked problem nodes:
  - `P2 Backside Resource Allocation`
  - `P3 Timing Closure Sensitivity`
  - `P4 Dynamic Power Reduction Under Constraints`
  - `P8 Generalization & Transferability`

5. `docs/knowledge_base/96_METHOD_LANDSCAPE.md`
- strongest linked method families:
  - `M3 Backside Cost/Predictor Modeling`
  - `M5 A/B + Causal Validation`
  - `M6 Stage-Gated Flow Integration`

## Current summarized narrative

The working paper narrative is:
1. `CTS-backside-only` may provide less value than moving a selected subset of signal nets to backside
2. this narrative is valid only if:
  - the physical contract is coherent
  - the PDN contract is not silently broken
  - backside usage is directly evidenced

This skill should therefore treat attribution as a gated mechanism judgment, not just a scoreboard readout.

## Newly added local papers worth reusing

1. `docs/papers/summaries/GOALPlace_Begin_with_the_End_in_Mind.summary.md`
- supports constrained objective design driven by downstream quality rather than local proxy metrics

2. `docs/papers/summaries/DREAM-GAN_Advancing_DREAMPlace_towards_Commercial-Quality_using_Generative_Adversarial_Learning.summary.md`
- strongest immediate local reference for "placement-stage gain must survive to post-route"

3. `docs/papers/summaries/Critical_Path_Aware_Timing_Driven_Global_Placement_for_Large-Scale_Heterogeneous_FPGAs.summary.md`
- useful for path-aware benefit scoring beyond simple net-length reasoning

4. `docs/papers/summaries/Bridging_the_Initialization_Gap_A_Co-Optimization_Framework_for_Mixed-Size_Global_Placement.summary.md`
- useful if future backside-aware placement benefits depend on staged introduction rather than one-shot objective activation

5. `docs/papers/summaries/LEGALM_Efficient_Legalization_for_Mixed-Cell-Height_Circuits_with_Linearized_Augmented_Lagrangian_Method.summary.md`
6. `docs/papers/summaries/Mixed-Cell-Height_Legalization_on_CPU-GPU_Heterogeneous_Systems.summary.md`
7. `docs/papers/summaries/A_Fast_Optimal_Double_Row_Legalization_Algorithm.summary.md`
- together these three papers anchor the rule that attribution claims must survive legalization/runtime reality, not just placement-stage scoring
