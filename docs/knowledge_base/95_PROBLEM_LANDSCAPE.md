# Problem Landscape (Auto-Synced)

- last_sync: `2026-03-07 20:32:13`
- source: `docs/papers/summaries/*.summary.md`
- papers_scanned: `26`

## Landscape Nodes
| id | problem | evidence_papers | linked_methods |
|---|---|---:|---|
| P1 | Routing Capacity & Congestion | 10 | M1,M2,M3,M4,M5,M6 |
| P2 | Backside Resource Allocation | 26 | M1,M2,M3,M4,M5,M6,M7 |
| P3 | Timing Closure Sensitivity | 19 | M1,M2,M3,M4,M5,M6,M7 |
| P4 | Dynamic Power Reduction Under Constraints | 9 | M1,M3,M4,M5 |
| P5 | Via/TSV & Interconnect Constraints | 16 | M1,M3,M4,M5,M6,M7 |
| P6 | Legality & Detailed Placement Robustness | 5 | M1,M3,M4,M5,M6,M7 |
| P7 | Cross-Domain Risks | 10 | M1,M3,M4,M5,M7 |
| P8 | Generalization & Transferability | 22 | M1,M2,M3,M4,M5,M6,M7 |

## Node Details
### P1 Routing Capacity & Congestion
- description: Routing demand exceeds available resources, causing overflow/hotspots.
- matched_papers: `10`
- examples:
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - GOALPlace: Begin with the End in Mind
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges
  - RePlAce: Advancing Solution Quality and Routability Validation in Global Placement
  - Scaled FinFETs Connected by Using Both Wafer Sides for Routing via Buried Power Rails
  - Timing-Driven Global Placement by Efficient Critical Path Extraction

### P2 Backside Resource Allocation
- description: Need principled front-vs-back net assignment under finite backside resources.
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

### P3 Timing Closure Sensitivity
- description: QoR highly sensitive to critical-path and clock-data interaction under placement/routing changes.
- matched_papers: `19`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - Critical Path Aware Timing-Driven Global Placement for Large-Scale Heterogeneous FPGAs
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - DREAM-GAN: Advancing DREAMPlace towards Commercial-Quality using Generative Adversarial Learning
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node

### P4 Dynamic Power Reduction Under Constraints
- description: Lower dynamic power without area/timing regression.
- matched_papers: `9`
- examples:
  - A Two Moment RC Delay Metric for Performance Optimization
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node
  - Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges
  - Modeling the “Effective Capacitance” for the RC Interconnect of CMOS Gates
  - Performance Computation for Precharacterized CMOS Gates with RC Loads
  - Power Delivery Network (PDN) Modeling for Backside-PDN Configurations With Buried Power Rails and µTSVs

### P5 Via/TSV & Interconnect Constraints
- description: nTSV/via and interconnect parasitics constrain backside benefits.
- matched_papers: `16`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - A Two Moment RC Delay Metric for Performance Optimization
  - Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators
  - Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node
  - GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment
  - IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs

### P6 Legality & Detailed Placement Robustness
- description: Global-placement gains may vanish if legalization/detailed placement is unstable.
- matched_papers: `5`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay
  - LEGALM: Efficient Legalization for Mixed-Cell-Height Circuits with Linearized Augmented Lagrangian Method
  - Mixed-Cell-Height Legalization on CPU-GPU Heterogeneous Systems

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
- matched_papers: `22`
- examples:
  - A Fast Optimal Double Row Legalization Algorithm
  - A Holistic Evaluation of Buried Power Rails and Back-Side Power for Sub-5 nm Technology Nodes
  - A Two Moment RC Delay Metric for Performance Optimization
  - BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers
  - Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling
  - Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay
  - Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond
  - Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm
  - Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration
  - Critical Path Aware Timing-Driven Global Placement for Large-Scale Heterogeneous FPGAs

