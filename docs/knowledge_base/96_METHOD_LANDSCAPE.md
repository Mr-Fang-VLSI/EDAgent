# Method Landscape (Auto-Synced)

- last_sync: `2026-03-06 11:44:16`
- source: `docs/papers/summaries/*.summary.md`
- papers_scanned: `15`

## Landscape Nodes
| id | method family | evidence_papers | addresses_problems |
|---|---|---:|---|
| M1 | Objective Shaping in Placement | 10 | P1,P2,P3,P4,P5,P6,P7,P8 |
| M2 | Local Resource-Aware Modeling | 1 | P1,P2,P3,P8 |
| M3 | Backside Cost/Predictor Modeling | 15 | P1,P2,P3,P4,P5,P6,P7,P8 |
| M4 | Constraint-Guided Optimization | 11 | P1,P2,P3,P4,P5,P6,P7,P8 |
| M5 | A/B + Causal Validation | 12 | P1,P2,P3,P4,P5,P6,P7,P8 |
| M6 | Stage-Gated Flow Integration | 2 | P1,P2,P3,P5,P8 |
| M7 | Legalization/DP Strategy | 1 | P2,P3,P6,P7,P8 |

## Node Details
### M1 Objective Shaping in Placement
- description: Modify objective with domain-aware terms instead of pure HPWL.
- matched_papers: `10`
- examples:
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs
  - Power Delivery Network (PDN) Modeling for Backside-PDN Configurations With Buried Power Rails and µTSVs
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement
  - Scaled FinFETs Connected by Using Both Wafer Sides for Routing via Buried Power Rails
  - Timing-Driven Global Placement by Efficient Critical Path Extraction

### M2 Local Resource-Aware Modeling
- description: Use local density/capacity/congestion proxies to guide optimization.
- matched_papers: `1`
- examples:
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement

### M3 Backside Cost/Predictor Modeling
- description: Build front-vs-back delay/power proxy models with stability gates.
- matched_papers: `15`
- examples:
  - A Holistic Evaluation of Buried Power Rails and Back-Side Power for Sub-5 nm Technology Nodes
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs

### M4 Constraint-Guided Optimization
- description: Use hard/soft constraints (timing, risk budget, policy lock) to prevent invalid wins.
- matched_papers: `11`
- examples:
  - A Holistic Evaluation of Buried Power Rails and Back-Side Power for Sub-5 nm Technology Nodes
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges

### M5 A/B + Causal Validation
- description: Use paired experiments/ablation to isolate mechanism and avoid confounding.
- matched_papers: `12`
- examples:
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges
  - Power Delivery Network (PDN) Modeling for Backside-PDN Configurations With Buried Power Rails and µTSVs
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement

### M6 Stage-Gated Flow Integration
- description: Integrate method through reproducible stage checkpoints and promotion gates.
- matched_papers: `2`
- examples:
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement

### M7 Legalization/DP Strategy
- description: Use explicit detailed placement/legalization strategy (e.g., NTUplace3/ABCDPlace fallback).
- matched_papers: `1`
- examples:
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers

