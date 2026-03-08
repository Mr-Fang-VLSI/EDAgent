# Method Landscape (Auto-Synced)

- last_sync: `2026-03-07 20:32:13`
- source: `docs/papers/summaries/*.summary.md`
- papers_scanned: `26`

## Landscape Nodes
| id | method family | evidence_papers | addresses_problems |
|---|---|---:|---|
| M1 | Objective Shaping in Placement | 17 | P1,P2,P3,P4,P5,P6,P7,P8 |
| M2 | Local Resource-Aware Modeling | 2 | P1,P2,P3,P8 |
| M3 | Backside Cost/Predictor Modeling | 26 | P1,P2,P3,P4,P5,P6,P7,P8 |
| M4 | Constraint-Guided Optimization | 16 | P1,P2,P3,P4,P5,P6,P7,P8 |
| M5 | A/B + Causal Validation | 15 | P1,P2,P3,P4,P5,P6,P7,P8 |
| M6 | Stage-Gated Flow Integration | 6 | P1,P2,P3,P5,P6,P8 |
| M7 | Legalization/DP Strategy | 4 | P2,P3,P5,P6,P7,P8 |

## Node Details
### M1 Objective Shaping in Placement
- description: Modify objective with domain-aware terms instead of pure HPWL.
- matched_papers: `17`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Bridging the Initialization Gap: A Co-Optimization Framework for Mixed-Size Global Placement
  - Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - Critical Path Aware Timing-Driven Global Placement for Large-Scale Heterogeneous FPGAs
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - DREAM-GAN: Advancing DREAMPlace towards Commercial-Quality using Generative Adversarial Learning
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment

### M2 Local Resource-Aware Modeling
- description: Use local density/capacity/congestion proxies to guide optimization.
- matched_papers: `2`
- examples:
  - GOALPlace: Begin with the End in Mind
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement

### M3 Backside Cost/Predictor Modeling
- description: Build front-vs-back delay/power proxy models with stability gates.
- matched_papers: `26`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - A Holistic Evaluation of Buried Power Rails and Back-Side Power for Sub-5 nm Technology Nodes
  - A Two Moment RC Delay Metric for Performance Optimization
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Bridging the Initialization Gap: A Co-Optimization Framework for Mixed-Size Global Placement
  - Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration

### M4 Constraint-Guided Optimization
- description: Use hard/soft constraints (timing, risk budget, policy lock) to prevent invalid wins.
- matched_papers: `16`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - A Holistic Evaluation of Buried Power Rails and Back-Side Power for Sub-5 nm Technology Nodes
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Bridging the Initialization Gap: A Co-Optimization Framework for Mixed-Size Global Placement
  - Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators

### M5 A/B + Causal Validation
- description: Use paired experiments/ablation to isolate mechanism and avoid confounding.
- matched_papers: `15`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - DREAM-GAN: Advancing DREAMPlace towards Commercial-Quality using Generative Adversarial Learning
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - GOALPlace: Begin with the End in Mind
  - IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs

### M6 Stage-Gated Flow Integration
- description: Integrate method through reproducible stage checkpoints and promotion gates.
- matched_papers: `6`
- examples:
  - Bridging the Initialization Gap: A Co-Optimization Framework for Mixed-Size Global Placement
  - DREAM-GAN: Advancing DREAMPlace towards Commercial-Quality using Generative Adversarial Learning
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - GOALPlace: Begin with the End in Mind
  - LEGALM: Efficient Legalization for Mixed-Cell-Height Circuits with Linearized Augmented Lagrangian Method
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement

### M7 Legalization/DP Strategy
- description: Use explicit detailed placement/legalization strategy (e.g., NTUplace3/ABCDPlace fallback).
- matched_papers: `4`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - LEGALM: Efficient Legalization for Mixed-Cell-Height Circuits with Linearized Augmented Lagrangian Method
  - Mixed-Cell-Height Legalization on CPU-GPU Heterogeneous Systems

