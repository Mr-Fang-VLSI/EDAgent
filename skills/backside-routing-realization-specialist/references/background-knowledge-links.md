# Background Knowledge Links

This skill should stay grounded in the current backside-routing realization problem rather than drifting into generic routing theory.

## Primary KB anchors

1. `docs/knowledge_base/107_BSPDN_TOPOLOGY_AND_BENEFIT_VALIDATION_PROGRAM_20260307.md`
- Gate B and the later post-route oracle work define why route realization is a separate stage between theory and placement promotion

2. `docs/knowledge_base/20_LAYER_POLICY_CTS_PDN_BACKSIDE.md`
- locks the current routing contract:
  - `BPR = PDN only`
  - `clock = M4+`
  - `backside signal = BM2/BM1 only`

3. `docs/knowledge_base/30_BACKSIDE_VIA_CONNECTIVITY_CHECKLIST.md`
- keeps the routing work tied to actual via/layer connectivity instead of abstract intent

4. `docs/knowledge_base/95_PROBLEM_LANDSCAPE.md`
- strongest linked problem nodes:
  - `P2 Backside Resource Allocation`
  - `P3 Timing Closure Sensitivity`
  - `P5 Flow Realization Gap`

5. `docs/knowledge_base/96_METHOD_LANDSCAPE.md`
- strongest linked method families:
  - `M3 Backside Cost/Predictor Modeling`
  - `M5 A/B + Causal Validation`
  - `M6 Stage-Gated Flow Integration`

## Local experiment anchors

1. `slurm_logs/04_delay_modeling/postroute_oracle_s8_top1_20260307.conclusion.md`
2. `slurm_logs/04_delay_modeling/postroute_oracle_s8_top10_20260307.conclusion.md`
- establish the current `selection bookkeeping only` failure mode for targeted reroute

3. `slurm_logs/04_delay_modeling/manual_patch_oracle_s8_top1_retry1_20260307.conclusion.md`
4. `slurm_logs/04_delay_modeling/manual_patch_oracle_s8_top1_retry1_20260307.experience_delta.md`
5. `slurm_logs/04_delay_modeling/manual_patch_oracle_s8_top1_retry2_20260307.monitor.md`
- show why raw DEF patching was able to preserve geometry but still failed connectivity/extraction

## Tool/source anchors

1. `scripts/debug/manual_backside_patch_oracle.py`
- previous manual patch path and its failure modes

2. `scripts/debug/sanitize_def_for_openroad.py`
- current compatibility bridge from Innovus routed DEF to OpenROAD-readable DEF

3. `scripts/debug/openroad_backside_rerouter.py`
- emerging local rerouter/wire-rewrite engine

4. `external_tools/OpenROAD-flow-scripts/tools/OpenROAD/src/drt/src/io/io.cpp`
- `io::Writer::updateDbConn(...)` is the most relevant reference for dbWire/dbWireEncoder-backed route materialization

5. `external_tools/OpenROAD-flow-scripts/tools/OpenROAD/src/odb/test/test_wire_codec.tcl`
6. `external_tools/OpenROAD-flow-scripts/tools/OpenROAD/src/odb/test/tcl/13-wire_encoder_test.tcl`
- minimal OpenDB wire-encoding references, more useful than full TritonRoute internals for the current rerouter bring-up

## RC-aware measurement anchors

When route realization must be judged electrically rather than geometrically, use:

1. `docs/papers/summaries/Modeling_the_Effective_capacitance_for_the_RC_interconnect_of_CMOS_gates.summary.md`
2. `docs/papers/summaries/Performance_computation_for_precharacterized_CMOS_gates_with_RC_loads.summary.md`
3. `docs/papers/summaries/A_Two_Moment_RC_Delay_Metric_for_Performance_Optimization.summary.md`
4. `docs/papers/summaries/Buffer_placement_in_distributed_RC-tree_networks_for_minimal_Elmore_delay.summary.md`

These papers matter because route-realization success is not just `BM1/BM2` occupancy; it must eventually survive extracted RC comparison with fanout/tree structure and access-via penalties included.

## Local code structure this skill must understand

This expert skill is expected to understand and modify the current local routing stack:

1. `scripts/debug/openroad_backside_rerouter.py`
- local OpenROAD/OpenDB-backed net wire rewrite engine

2. `scripts/debug/sanitize_def_for_openroad.py`
- compatibility bridge from Innovus routed DEF to OpenROAD-readable DEF

3. `scripts/debug/manual_backside_patch_oracle.py`
- older manual patch path; still useful as a failure-mode reference and fallback

4. `scripts/debug/analyze_backside_net_delay.py`
- current per-net electrical comparison helper for front vs patched/oracle views

5. `scripts/stages/innovus/run.sh`
- replay contract and stage semantics that determine whether patched or rerouted DEFs are actually measured correctly

6. `scripts/stages/innovus/run_openroad_cts_bridge.sh`
- existing OpenROAD bridge pattern that shows how the repo already interacts with OpenROAD tooling

## Current summarized narrative

The current routing-realization narrative is:
1. theory can predict backside-eligible nets,
2. the current industrial flow may still fail to realize `BM2/BM1` occupancy,
3. therefore a local routing-realization layer is needed between theory and final placement claims,
4. that layer should prefer tool-backed wire construction over repeated hand-edited DEF text once compatibility is established,
5. and the expert skill should be able to directly repair that local realization stack rather than only report on it.
