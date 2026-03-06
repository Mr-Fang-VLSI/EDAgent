# AutoIdea Fusion Report

- timestamp: `2026-03-06 11:51:54`
- autoidea_root: `external_tools/autoIdea`
- imported_recommendation_count: `24`
- merged_queue_count: `87`

## Imported Artifacts
- paper recommendation queue: `docs/papers/queues/autoidea_recommended_top30_bridge.tsv`
- merged retrieval queue: `docs/papers/queues/literature_feedback_merged_with_autoidea.tsv`
- this report: `docs/knowledge_base/99_AUTOIDEA_FUSION_REPORT_20260306.md`

## Strengths Borrowed from autoIdea
1. Citation/semantic expansion around local corpus (`recommended_top30`).
2. Structured problem-formulation abstraction from historical literature.
3. Debate-style idea and experiment draft generation.

## Fusion Mapping into Current Skill Stack
- `eda-paper-fetch`: prioritize `autoidea_recommended_top30_bridge.tsv` for targeted download.
- `paper_kb_index` + landscape pipeline: absorb downloaded/summarized papers into 95/96/97/98 artifacts.
- `eda-idea-debate-lab` / `eda-hypothesis-experiment-designer`: use imported idea+experiment draft as initial candidate, then apply theory veto and non-regression gates.

## Imported Idea Draft (from autoIdea)
```text
<motivation>
BSPDN promises large IR-drop relief and routability gains, but current flows either lock into template meshes or optimize limited knobs (e.g., grid width) without jointly planning nTSV farms, backside mesh topology, and multifunctional layer roles. PDN-last strategies improve signal QoR, yet they still lack a fast, signoff-correlated way to co-optimize nTSV placement/sizing under overlay/DFM and EM constraints while accounting for dynamic, workload-driven droop. As a result, designs are over-provisioned in nTSVs and metal, late-stage DFM escapes occur due to overlay sensitivity, and backside clock/power coexistence is handled by ad hoc rules rather than by jitter/coupling-aware optimization.
</motivation>

<novelty>
We propose a single, PDN-last-friendly co-synthesis loop that is both nTSV-aware and distributionally robust to dynamic workloads, using differentiable surrogates calibrated to signoff and explicit overlay/DFM yield constraints. Unlike prior RL-only width tuning, fixed-template PDNs, or clock-only backside methods, our approach jointly decides regional nTSV farm geometry, backside mesh sizing/topology, and per-tile layer role assignment (power/clock/shield) while trading off IR-drop, EM/thermal limits, routability, and clock jitter. It treats overlay and etch variability as part of the objective via stochastic constraints, and emits regularized, DFM-clean nTSV patterns with planned spares for ECO. The result is a unified optimizer that can cut nTSV/metal usage and jitter simultaneously while maintaining PDN-last routability guarantees.
</novelty>

<method>
We train multi-physics neural operators that predict 3D voltage, temperature, and nTSV/metal current densities for many activity waveforms, calibrated online to golden IR/EM/thermal solvers with uncertainty gating. The optimization variables include per-region nTSV pitch/diameter/offset (with capture-pad sizing), backside mesh widths/pitches per layer, coarse mesh topology seeds, and a discrete per-tile mask that assigns layers to power, clock, or shield; spare nTSV sites are also selected for ECO. We minimize worst-quantile (e.g., Q95) dynamic droop subject to Lagrangian penalties for EM, thermal, and routability, and enforce overlay/DFM robustness by sampling misalignment/etch distributions during training and optimization; discrete decisions are relaxed via Gumbel-Softmax while coarse topology seeds are refined by a lightweight RL policy. The flow is PDN-last: we reserve minimal backside blockages early, run signal/clock routing, then re-optimize with updated congestion and jitter costs to finalize nTSV farms, mesh sizing, and layer roles. The tool outputs DRC-clean layouts with regularized nTSV arrays, shielded clock corridors, and spare pillar straps, and validates final designs with signoff-in-the-loop and ECO hooks to activate spares if silicon sensors detect unexpected droop.
```

## Imported Experiment Draft (from autoIdea)
```text
### Refined Experiment Design

1. **Problem Setup**
   - **Objective**: Co-synthesize nTSV farms, backside mesh topology/sizing, and per-tile layer role assignment (power/clock/shield) in a PDN-last flow to minimize worst-quantile dynamic IR-drop while meeting stringent reliability criteria including electromigration (EM), thermal management, DFM/overlay tolerances, routability, and clock jitter constraints.
   - **Decision Variables**:
     - **nTSV**: per-region pitch, diameter, keep-out/capture-pad size, offset/phase; spare-site selection density and placement regularity. Incorporate minimum spacing rules derived from [Buried_Power_Rails_and_Nano-Scale_TSV_Technology_Boosters_for_Backside_Power_Delivery_Network_and_3D_Heterogeneous_Integration](https://doi.org/10.1109/TED.2020.3090070).
     - **Backside Mesh**: width/pitch per backside metal layer; coarse topology seeds (mesh vs hybrid H-tree corridors) inspired by [Buried_Power_Rails_and_Back-side_Power_Grids_Prospects_and_Challenges](https://arxiv.org/abs/2004.05210).
     - **Layer Roles**: discrete per-tile mask for power, clock, or shield on selected backside layers, incorporating insights from [Power-CAD_A_novel_methodology_for_design_analysis_and_optimization_of_Power_Electronic_Module_layouts](https://doi.org/10.1109/WHISPERS.2020.9386143).
   - **Workload Model**: Set of dynamic activity traces per design block (burst, periodic, and adversarial patterns). Model power profiles using realistic workload scenarios from SPECint/fp and MLPerf kernels, ensuring comprehensive stress testing under varying conditions for worst-quantile objectives (Q95/Q99).
   - **Surrogates**: Multi-physics neural operators for voltage, temperature, and current density; uncertainty-gated online calibration with golden IR/EM/thermal solvers to improve prediction fidelity, referencing [OpeNPDN_A_Neural-Network-Based_Framework_for_Power_Delivery_Network_Synthesis](https://doi.org/10.1109/TED.2019.2915123).
   - **Robustness**: Stochastic constraints for overlay and etch bias via Monte Carlo sampling during optimization, influenced by [Accelerating design-technology co-development using neural compact modeling and data-driven SPICE simulation](https://doi.org/10.1109/IEDM.2019.8993529). The flow remains PDN-last: early minimal backside reservation is made to accommodate later PDN kinematics.
   - **Deliverables**: DRC-clean layouts with regularized nTSV arrays, shielded clock corridors, and spare pillars; signoff validation and ECO hooks for activating spares in response to silicon sensor-detected droops.

2. **Benchmarks (PDN, routing, nTSV-aware flows)**
   - **Designs**:
     - CPU tile: out-of-order core + L2 slice (10–50 mm^2 variants) modeled after industry-standard cores.
     - AI accelerator: systolic MAC array + SRAM banks (small/medium/large) with realistic power profiles.
     - GPU shader cluster slice emphasizing heat distribution and dynamic power profiles.
     - IO/SoC subsystem block with mixed power profiles leveraging insights from [Chiplet_Interposer_Co-Design_for_Power_Delivery_Network_Optimization_in_Heterogeneous_2.5-D_ICs](https://doi.org/10.1109/DAC.2020.147124).
     - Open-source surrogates: OpenROAD/ISPD’18/19 routability benchmarks adapted with power maps; EPFL/IBEX/Ariane cores; NVDLA (small).
   - **Technology Nodes**:
     - Explore 5/3/2 nm class FinFET/GAA PDK proxies with backside capabilities; backside metal pitch: 160–320 nm; nTSV diameter: 0.4–1.2 µm; aspect ratio 5–10; overlay sigma 2–6 nm.
   - **Power/Activity**:
     - Utilize realistic vectors from SPECint/fp and MLPerf kernels, including synthetic di/dt bursts and randomized toggling; 100–500 waveform scenarios per design to thoroughly investigate dynamic behavior.
   - **Flows**:
     - Frontside: standard PnR up to routed clocks/signals with PDN-last reservations derived from [Design and Technology Co-Optimization Utilizing Multi-Bit Flip-Flop Cells](https://doi.org/10.1007/s10799-021-00301-x).
     - nTSV-aware: custom generator to insert farm arrays as obstructions and extraction anchors for parasitic coupling modeling for clock corridors and shields.
     - Signoff: golden IR-drop/EM/thermal solvers; STA with SI and clock-jitter decomposition; DRC/DFM decks; CMP/density/overlay checks.
   - **Data for Surrogate Training**:
     - 1,000–3,000 layout-activity pairs per node across multi-load corners (V/T), with signoff labels for V/T/current density; hold out 20% of designs for validation and 10% stress tests with extreme overlay and workload.

3. **Baselines (ML or traditional EDA)**
   - **B1**: Fixed-template BSPDN mesh with uniform nTSV pitch, utilizing heuristic guard-bands.
   - **B2**: RL-only width tuning on a fixed mesh topology; no nTSV co-optimization or layer-role decisions, reinforcing findings from [Macro-Aware_Row-Style_Power_Delivery_Network_Design_for_Better_Routability](https://doi.org/10.1109/TED.2021.3065630).
   - **B3**: PDN-first frontside-optimized grid (traditional) + standard backside mesh; only using the front-side for clock routing to validate against emerging methodologies.
   - **B4**: Backside clock-only method with frontside power grid; heuristic shielding; no joint optimization.
   - **B5**: Deterministic optimization of backside mesh widths + nTSV pitch using convex/Lagrangian solver without stochastic overlay modeling or discrete layer-role masks.
   - **B6**: ILP/CP for nTSV placement and mesh sizing on a small block, without dynamic workloads or joint optimization.
   - **B7**: Heuristic ECO spare insertion (uniform 5–10% spare nTSVs) without co-design, relying on traditional methods.

4. **Evaluation Metrics (IR-drop, thermal hotspot count, congestion)**
   - **Power Integrity**:
     - Dynamic IR-drop: Monitor metrics like Q50, Q90, Q95, and Q99 per block; assess worst-case droop; measure Vmin headroom.
     - Static IR-drop: Calculate mean/max values using golden solvers as a benchmark.
     - IR-drop tail sensitivity: Evaluate the difference between average and top-quantile millivolts to understand workload impact.
   - **EM/Thermal**:
     - EM violation count and worst margin (current density in mA/µm over the established limit).
     - Assess peak temperature, thermal gradient (ΔT), and hotspot count within areas exceeding 95 C or specific PDK thresholds.
   - **Clock/Signals**:
     - Calculate clock skew, insertion delay, and jitter components (supply-induced jitter, crosstalk-induced jitter); track jitter budget violations.
     - Monitor signal SI noise events on critical nets near backside corridors to ensure reliability.
   - **Routability/DRC/DFM**:
     - Analyze global/detailed routing overflows; account for via counts, detours, and wirelength metrics.
     - Review DRC violations (shorts/spaces/vias/antenna/CMP/density windows) to maintain design rules.
     - Overlay robustness: Compute yield proxy under misalignment distribution (pass rates across N Monte Carlo samples), reporting minimum overlay margins.
     - Pattern regularity score for nTSV farms; assess spare activation reachability with practical use cases.
   - **Cost/Area**:
     - Count nTSVs and occupied area; analyze backside metal area usage; gauge layer-role utilization; partition power/clock metal shares.
     - Measure runtime overhead (optimization + calibration calls) compared to signoff-only loops to evaluate efficiency.

5. **Ablation Studies**
   - **A1**: Remove stochastic overlay/etch modeling (use deterministic approaches only) to evaluate impact on robustness.
   - **A2**: Exclude per-tile layer-role assignment (assume power-only backside) to analyze optimization outcomes.
   - **A3**: Omit shield corridors; analyze performance with an unshielded clock on the backside.
   - **A4**: Conduct mesh-only optimization while fixing nTSV farms to assess the importance of integrated optimization.
   - **A5**: Implement nTSV-only optimization while fixing mesh widths/topology for comparative analysis.
   - **A6**: Eliminate spare planning and ECO hooks to understand flexibility impacts on designs.
   - **A7**: Disallow PDN-last re-optimization (perform a single-shot optimization prior to routing) to quantify impacts on routability.
   - **A8**: Remove uncertainty gating and online calibration; maintain a frozen surrogate to measure fidelity impacts.
   - **A9**: Substitute Gumbel-Softmax with straight-through rounding to assess optimization flexibility lost.
   - **A10**: Remove RL topology refinement; preserve gradient-only continuous knobs to evaluate optimization boundaries.
   - **A11**: Train with static workloads only and evaluate performance on dynamic burst workloads to understand robustness.

6. **Sensitivity Studies for Technology Scaling**
   - **Node Scaling (5 → 3 → 2 nm proxies)**:
     - Adapt backside pitch shrink, metal resistivity increases, and shifts in via resistance.
     - Explore overlay sigma variations from 2 → 6 nm; both positive and negative etch bias variations (±2 → ±5 nm).
     - Evaluate power density increments (+20–50%) and clock frequency scaling (1.5–2.0x).
   - **nTSV Geometry**:
     - Investigate diameter variations (0.4–1.2 µm); aspect ratio shifts (5–10); assess keep-out radius of 1–3× diameter.
     - Analyze capture-pad size sensitivity and DRC spacing rules using findings from [Power Sub-Mesh Construction in Multiple Power Domain Design with IR Drop and Routability Optimization](https://doi.org/10.1109/TED.2021.3069714).
   - **Thermal Boundary Conditions**: Conduct evaluations on variations in thermal interface material (TIM) and heat-spreader conductivity (±30%).
   - **Generalization**:
     - Transfer a surrogate across nodes with light calibration vs. full retrain; measure impacts on accuracy and optimization quality.
   - **Robustness**:
     - Assess degradation in benefit under extreme overlay tails (P99.9); identify breakpoints requiring additional shielding or spare density.

7. **DRC or Timing-Aware Validations**
   - **DRC/DFM Signoff**:
     - Execute full rule decks: spacing, density/CMP windows, via arrays; apply enclosure checks and min-cut rules.
     - Conduct overlay checks: Monte Carlo misalignment assessments across backside-to-frontside; report both pass rates and worst offsets.
     - Perform patterning/EPE/etch bias-aware verifications for backside layers; ensure regularity constraints are satisfied based on [Backside_Design_Methodology_for_Power_Delivery_Network_and_Clock_Routing](https://doi.org/10.1109/TED.2020.2987847).
   - **EM/IR/Thermal Signoff**:
     - Execute vector-based dynamic IR simulations across the workload suite with golden solvers; calculate EM margins per segment/nTSV; simulate thermal steady-state and transient regimes.
     - Correlate surrogate predictions with signoff metrics: evaluate RMSE and maximum error along with Q95 error, aiming for <5 mV RMSE and <10 mV Q95 error before finalization.
   - **STA with SI and Power-Aware Jitter**:
     - Compute timing at multiple PVTs; include supply-induced jitter and crosstalk; review slack distributions for violations.
     - Validate clock QoR through skew/jitter budgets and insertion delays; examine coupling effects on power corridors to confirm shielding efficacy.
   - **ECO Validation**:
     - Simulate silicon-sensor-like droop injections and activate spares; recheck IR/EM/clock impacts alongside new DRC/SI violations to ensure compliance.

8. **Expected Results & Insights**
   - **Power Integrity and Resources**:
     - Anticipate a 20–35 mV reduction in Q95 dynamic IR-drop vs. fixed-template baseline; predict 10–20 mV reduction compared to RL width-tuning baseline.
     - Expect 15–30% fewer nTSVs and 10–20% less backside metal area while maintaining equal or improved droop metrics.
     - Reduce EM violations by 30–60%; aim to improve worst-segment EM margins by 10–25% through integrated methods.
   - **Clock/Routability**:
     - Project a 10–20% reduction in supply-induced jitter; maintain or improve skew/insertion delay metrics through optimized shielded corridors.
     - Predict a 5–15% reduction in global routing overflow with a 3–8% decrease in wirelength from PDN-last co-design.
   - **Robustness/DFM**:
     - Estimate a ≥95% pass rate under overlay Monte Carlo vs. 70–85% for non-robust methods; analyze late DFM escapes across designs.
     - Regularized farm patterns proposed to minimize DRC noise, ensuring that CMP/density windows remain within specification without extra fill.
   - **Surrogate Fidelity and Efficiency**:
     - Validate surrogate-signoff correlation with RMSE <5 mV and <3 C; reduce optimization runtime by 3–5× compared to signoff-in-loop-only baselines
```

## Imported Historical Formulation Notes
```text
Below is an abstraction of historical patterns, assumptions, and their breakdown at advanced nodes, followed by structured, domain-general summaries of the listed works.

---

## 1. Historical Problem Formulation Patterns (Generic, Abstract)

Across generations, EDA problems in placement, routing, power delivery, timing, and multi-die integration have tended to follow a limited set of abstract templates:

### 1.1 Single-Objective Physical Optimization
- **Canonical form**:  
  Minimize a single physical cost (e.g., wirelength, congestion, delay, IR drop, temperature) subject to basic design-rule and capacity constraints.
- **Typical simplifications**:
  - Lumped or linear models (e.g., linear delay vs. load, linear resistance networks).
  - Timing or power treated separately from geometry: first optimize layout, then analyze/patch.

### 1.2 Multi-Objective Tradeoff with Weighted Sum
- **Canonical form**:  
  Minimize a weighted sum of several proxies (e.g., wirelength + λ·timing + μ·power) under placement/routing legality constraints.
- **Key characteristic**:
  - Objectives are expressed via coarse, separable metrics.
  - Dependencies (e.g., between power and timing, or thermal and reliability) are often handled via static weights or staged flows, not coupled optimization.

### 1.3 Hierarchical / Decomposed Co-Optimization
- **Canonical form**:  
  Break the full problem into stages or hierarchies (chip → block → standard cell; package vs. chip; power vs. signal) with restricted feedback between levels.
- **Design pattern**:
  - Solve “sub-problems” in sequence: floorplan → global placement → clock-tree → routing → signoff.
  - Each stage uses simple views of upstream/downstream effects (e.g., margins, guard-bands, corner-based pessimism).

### 1.4 Graph/Network-Based Modeling with Static Features
- **Canonical form**:  
  Represent the design or a subsystem (netlist, grid, interconnect, power network, thermal path) as a graph or grid network and optimize a function over this structure.
- **EDAspecific twist**:
  - Simple node/edge features: scalar capacities, delays, or resistances.
  - Static or weakly dynamic models (e.g., no online retraining; minimal adaptivity across designs).

### 1.5 Rule-Driven / Heuristic Search
- **Canonical form**:  
  Use rule-based or heuristic search (e.g., greedy, simulated annealing, local refinement) to explore design choices with approximate cost evaluation.
- **Common traits**:
  - Cost functions rely on pre-characterized libraries and technology files.
  - Search space is constrained to preserve design-rule legality and rough timing closure.

### 1.6 Single-Domain Modeling
- **Canonical form**:  
  Treat power, timing, signal integrity, thermal, and mechanical stress mostly as separate problem domains.
- **Strategy**:
  - Perform domain-specific analyses; integrate via margins, worst-case corners, or post-processing fixes.
  - Avoid solving tightly coupled multi-physics or multi-domain problems in a single unified formulation.

---

## 2. Common Assumptions Across Generations

Several high-level assumptions have implicitly underpinned these formulations across many technology generations:

1. **Planar or Near-Planar Abstraction**
   - The design is effectively 2D with a fixed, small number of uniform metal layers.
   - Power and signal are largely separated by layer assignment and simple hierarchy.

2. **Weak Coupling Between Physical Domains**
   - Timing can be optimized largely independently of power integrity, thermal behavior, and mechanical effects.
   - Electrical and thermal problems can be solved iteratively but not fully co-optimized.

3. **Static and Homogeneous Technology Views**
   - Library cells are characterized under a limited set of global corners.
   - Interconnect stacks are assumed mostly uniform; local process variations are treated as small perturbations.
   - Standard PDK abstractions are sufficient for all design stages.

4. **Dominance of Front-Side Interconnect**
   - Signal routing and power delivery occur primarily on the same “side” of the device stack.
   - Power and clock structures live in well-defined subsets of front-side metal layers.

5. **Single-Die, Monolithic System View**
   - The chip is modeled as a single contiguous die.
   - Package and board are either abstracted as boundary conditions or treated in separate flows.

6. **Global, Lumped Timing and Power Models**
   - Delay and power are estimated using lumped models at cell or net granularity.
   - Local current densities, localized IR-drop, and local thermal hotspots are approximated or captured via margins rather than finely resolved field solutions.

7. **Stable Scaling Trends**
   - Interconnect scaling trends are assumed smooth; wiring can be “shrunk” with predictable RC behavior.
   - Power-density and thermal issues increase but remain manageable via incremental techniques.

8. **Moderate Design Complexity per Node**
   - The complexity increase per generation is incremental and can be absorbed by improved heuristics and faster hardware.
   - Traditional hierarchical decomposition remains sufficient to manage design size.

---

## 3. Assumptions That No Longer Hold at Advanced Nodes

At advanced nodes and in heterogeneous 2.5D/3D systems, several of the above assumptions break:

1. **Breakdown of Simple 2D Abstraction**
   - Vertical integration (3D integration, through-silicon structures, buried routing, backside networks) makes the design inherently 3D.
   - Power, signal, and thermal paths become strongly three-dimensional and intertwined.

2. **Strong Coupling Between Power, Timing, and Thermal**
   - IR drop directly perturbs timing, and local switching activity perturbs IR and temperature in complex, time-varying ways.
   - Thermal gradients and self-heating significantly affect device and interconnect behavior, undermining simple corners and margins.

3. **Non-Uniform, Heterogeneous Interconnect Stacks**
   - Mixed-pitch layers, specialized layers for power, clock, or high-speed signals, and non-uniform dielectric/metal stacks break simple uniform RC assumptions.
   - Backside routing and buried power structures introduce asymmetric constraints and complex via/through-silicon patterns.

4. **Multi-Die and Multi-Package Integration**
   - Chiplets and multi-package assemblies invalidate the single-die assumption.
   - Cross-die signaling, shared power delivery, and package-level constraints necessitate system-level co-design rather than local chip-only optimization.

5. **Local, Transient, and Activity-Dependent Effects Dominate**
   - Local power-density hotspots and dynamic IR/EM constraints cannot be handled by coarse, global margins.
   - The location and timing of switching activity across space and time matters for PDN integrity and thermal safety.

6. **Emergence of Backside Power Delivery and Specialized Power Fabrics**
   - Dedicated backside or buried power fabrics decouple, but also tightly couple, power and signal in new ways: power is moved “behind” the logic, changing routing constraints and EM/IR characteristics.
   - Design rules become more complex and asymmetric between front and backside.

7. **Classical Library-Based Characterization is Strained**
```

## Next Actions
1. Run `eda-paper-fetch` over top high-priority merged queue rows.
2. Download + summarize PDFs, then run `paper_kb_index.py build`.
3. Re-run `autoidea_bridge.py` and compare `98_LITERATURE_FEEDBACK_LOOP.md` gap counts.
