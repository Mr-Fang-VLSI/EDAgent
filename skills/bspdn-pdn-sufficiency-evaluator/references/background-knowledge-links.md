# Background Knowledge Links

This skill should stay anchored to the current PDN-sufficiency knowledge, not to informal interpretation.

## Primary KB anchors

1. `docs/knowledge_base/107_BSPDN_TOPOLOGY_AND_BENEFIT_VALIDATION_PROGRAM_20260307.md`
- Gate C defines the canonical PDN sufficiency question and experiment family

2. `docs/knowledge_base/20_LAYER_POLICY_CTS_PDN_BACKSIDE.md`
- current contract keeps:
  - `BPR` reserved for PDN
  - signal off `BPR`

3. `docs/knowledge_base/95_PROBLEM_LANDSCAPE.md`
- strongest linked problem nodes:
  - `P2 Backside Resource Allocation`
  - `P5 Via/TSV & Interconnect Constraints`
  - `P7 Cross-Domain Risks`

4. `docs/knowledge_base/96_METHOD_LANDSCAPE.md`
- relevant method families:
  - `M4 Constraint-Guided Optimization`
  - `M5 A/B + Causal Validation`
  - `M6 Stage-Gated Flow Integration`

## Current summarized knowledge

Current default interpretation:
1. `BPR` is a PDN-local resource, not a general signal layer
2. current PDN should be evaluated first under a strict contract
3. if `PDN-boost` helps and `Strict-BPR` does not, the fix should target PDN strength rather than signal/BPR mixing

This skill should therefore treat "PDN enough?" as its own first-class question.

## Newly added local papers worth reusing

1. `docs/papers/summaries/GOALPlace_Begin_with_the_End_in_Mind.summary.md`
- useful because it frames optimization against downstream outcomes rather than local heuristics only

2. `docs/papers/summaries/DREAM-GAN_Advancing_DREAMPlace_towards_Commercial-Quality_using_Generative_Adversarial_Learning.summary.md`
- useful as a persistence check reference: PDN interpretations should be judged by downstream effect, not early proxy wins alone

3. `docs/papers/summaries/LEGALM_Efficient_Legalization_for_Mixed-Cell-Height_Circuits_with_Linearized_Augmented_Lagrangian_Method.summary.md`
- useful because any PDN-side decision that destabilizes legalization or detailed placement is not "free"
