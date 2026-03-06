# Problem Landscape (Auto-Synced)

- last_sync: `2026-03-06 11:44:16`
- source: `docs/papers/summaries/*.summary.md`
- papers_scanned: `15`

## Landscape Nodes
| id | problem | evidence_papers | linked_methods |
|---|---|---:|---|
| P1 | Routing Capacity & Congestion | 9 | M1,M2,M3,M4,M5,M6 |
| P2 | Backside Resource Allocation | 15 | M1,M2,M3,M4,M5,M6,M7 |
| P3 | Timing Closure Sensitivity | 11 | M1,M2,M3,M4,M5,M6,M7 |
| P4 | Dynamic Power Reduction Under Constraints | 5 | M1,M3,M4,M5 |
| P5 | Via/TSV & Interconnect Constraints | 10 | M1,M3,M4,M5,M6 |
| P6 | Legality & Detailed Placement Robustness | 1 | M1,M3,M4,M5,M7 |
| P7 | Cross-Domain Risks | 10 | M1,M3,M4,M5,M7 |
| P8 | Generalization & Transferability | 14 | M1,M2,M3,M4,M5,M6,M7 |

## Node Details
### P1 Routing Capacity & Congestion
- description: Routing demand exceeds available resources, causing overflow/hotspots.
- matched_papers: `9`
- examples:
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement
  - Scaled FinFETs Connected by Using Both Wafer Sides for Routing via Buried Power Rails
  - Timing-Driven Global Placement by Efficient Critical Path Extraction

### P2 Backside Resource Allocation
- description: Need principled front-vs-back net assignment under finite backside resources.
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

### P3 Timing Closure Sensitivity
- description: QoR highly sensitive to critical-path and clock-data interaction under placement/routing changes.
- matched_papers: `11`
- examples:
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement
  - Scaled FinFETs Connected by Using Both Wafer Sides for Routing via Buried Power Rails

### P4 Dynamic Power Reduction Under Constraints
- description: Lower dynamic power without area/timing regression.
- matched_papers: `5`
- examples:
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges
  - Power Delivery Network (PDN) Modeling for Backside-PDN Configurations With Buried Power Rails and µTSVs

### P5 Via/TSV & Interconnect Constraints
- description: nTSV/via and interconnect parasitics constrain backside benefits.
- matched_papers: `10`
- examples:
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges
  - Power Delivery Network (PDN) Modeling for Backside-PDN Configurations With Buried Power Rails and µTSVs
  - Scaled FinFETs Connected by Using Both Wafer Sides for Routing via Buried Power Rails

### P6 Legality & Detailed Placement Robustness
- description: Global-placement gains may vanish if legalization/detailed placement is unstable.
- matched_papers: `1`
- examples:
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers

### P7 Cross-Domain Risks
- description: Thermal/security/reliability effects can veto aggressive backside usage.
- matched_papers: `10`
- examples:
  - A Holistic Evaluation of Buried Power Rails and Back-Side Power for Sub-5 nm Technology Nodes
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges
  - Power Delivery Network (PDN) Modeling for Backside-PDN Configurations With Buried Power Rails and µTSVs
  - Scaled FinFETs Connected by Using Both Wafer Sides for Routing via Buried Power Rails

### P8 Generalization & Transferability
- description: Benchmark improvements may not transfer across designs/flows.
- matched_papers: `14`
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

