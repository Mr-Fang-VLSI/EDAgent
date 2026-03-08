# Tool / Flow Script Catalog

Auto-generated from `scripts/` by `scripts/common/tool_catalog.py`.

## Quick usage
- Rebuild: `python3 scripts/common/tool_catalog.py build`
- Query: `python3 scripts/common/tool_catalog.py query cts route`
- Query with facets: `python3 scripts/common/tool_catalog.py query monitor --stage analysis --lifecycle active`

## Summary

| type | count |
|---|---:|
| common_utility | 23 |
| debug_tool | 132 |
| flow_orchestrator | 2 |
| flow_stage | 6 |
| flow_stage_aux | 14 |
| flow_stage_tcl | 5 |
| script | 7 |
| tech_utility | 9 |

## common_utility

| tool_id | lifecycle | version | stage | path | summary |
|---|---|---|---|---|---|
| `common_adjust_clock_period_py` | active | 0.1.0 | cts | `scripts/common/adjust_clock_period.py` | adjust clock period |
| `autoidea_bridge` | active | 1.0.0 | analysis | `scripts/common/autoidea_bridge.py` | Bridge autoIdea recommendations and idea drafts into local queues/knowledge artifacts |
| `build_agent_skill_bundle` | active | 1.0.0 | analysis | `scripts/common/build_agent_skill_bundle.py` | Export standalone agent+skill bundle with skill-local mirrored scripts |
| `common_check_design_package_py` | active | 0.1.0 | utility | `scripts/common/check_design_package.py` | check design package |
| `common_cleanup_sh` | active | 0.1.0 | utility | `scripts/common/cleanup.sh` | ============================================================ |
| `conda_project_env_report` | active | 1.0.0 | analysis | `scripts/common/conda_project_env_report.py` | Report project conda roots, envs, and package availability for reproducible workflow binding |
| `common_derive_innovus_tuning_py` | active | 0.1.0 | utility | `scripts/common/derive_innovus_tuning.py` | derive innovus tuning |
| `common_experiment_memory_py` | active | 0.1.0 | utility | `scripts/common/experiment_memory.py` | experiment memory |
| `infra_stack_guard` | active | 1.0.0 | preflight | `scripts/common/infra_stack_guard.py` | Audit core infrastructure integrity: agent policy, KB, tool registry, and skills |
| `common_init_research_chain_py` | active | 0.1.0 | utility | `scripts/common/init_research_chain.py` | init research chain |
| `common_knowledge_gate_sh` | active | 0.1.0 | utility | `scripts/common/knowledge_gate.sh` | knowledge gate |
| `maintenance_log_rollup` | active | 1.0.0 | analysis | `scripts/common/maintenance_log_rollup.py` | Summarize long markdown maintenance logs into denser rollup notes with candidate experience entries and principles |
| `paper_kb_index` | active | 1.0.0 | analysis | `scripts/common/paper_kb_index.py` | Build/query paper evidence index with keyword/semantic/logic modes |
| `paper_landscape_feedback` | active | 1.0.0 | analysis | `scripts/common/paper_landscape_feedback.py` | Detect literature gaps/stale methods and generate targeted retrieval queue |
| `paper_landscape_sync` | active | 1.0.0 | analysis | `scripts/common/paper_landscape_sync.py` | Sync problem/method landscapes from local paper summaries into linked KB artifacts |
| `common_prepare_innovus_sdc_py` | active | 0.1.0 | utility | `scripts/common/prepare_innovus_sdc.py` | Commands where the first numeric positional argument is a time value. |
| `common_research_chain_guard_py` | active | 0.1.0 | utility | `scripts/common/research_chain_guard.py` | research chain guard |
| `common_sbatch_cpu_research_sh` | active | 0.1.0 | utility | `scripts/common/sbatch_cpu_research.sh` | sbatch cpu research |
| `common_skill_adoption_monitor_py` | active | 0.1.0 | analysis | `scripts/common/skill_adoption_monitor.py` | skill adoption monitor |
| `common_skill_system_audit_py` | active | 0.1.0 | utility | `scripts/common/skill_system_audit.py` | skill system audit |
| `common_sync_repo_skills_to_codex_home_sh` | active | 0.1.0 | utility | `scripts/common/sync_repo_skills_to_codex_home.sh` | sync repo skills to codex home |
| `tool_catalog` | active | 1.1.0 | analysis | `scripts/common/tool_catalog.py` | Build/query governed tool catalog with lifecycle/version facets |
| `common_unified_kb_query_py` | active | 0.1.0 | utility | `scripts/common/unified_kb_query.py` | unified kb query |

## debug_tool

| tool_id | lifecycle | version | stage | path | summary |
|---|---|---|---|---|---|
| `debug_analyze_backside_crossover_vs_innovus_py` | active | 0.1.0 | analysis | `scripts/debug/analyze_backside_crossover_vs_innovus.py` | analyze backside crossover vs innovus |
| `debug_analyze_backside_net_delay_py` | active | 0.1.0 | analysis | `scripts/debug/analyze_backside_net_delay.py` | analyze backside net delay |
| `debug_analyze_prects_log_py` | active | 0.1.0 | cts | `scripts/debug/analyze_prects_log.py` | analyze prects log |
| `debug_analyze_route_backside_distributions_and_model_consistency_py` | active | 0.1.0 | route | `scripts/debug/analyze_route_backside_distributions_and_model_consistency.py` | analyze route backside distributions and model consistency |
| `debug_auto_fix_layer_namespace_for_gt3_py` | active | 0.1.0 | utility | `scripts/debug/auto_fix_layer_namespace_for_gt3.py` | High indices first to avoid partial replacements (e.g. metal1 in metal10). |
| `debug_backfill_manifest_metrics_py` | active | 0.1.0 | utility | `scripts/debug/backfill_manifest_metrics.py` | backfill manifest metrics |
| `debug_backside_layer_calibration_2pin_sh` | active | 0.1.0 | utility | `scripts/debug/backside_layer_calibration_2pin.sh` | Physical calibration sweep on one 2-pin (or short) net: |
| `debug_bapp_compare_vanilla_vs_precond_sh` | active | 0.1.0 | utility | `scripts/debug/bapp_compare_vanilla_vs_precond.sh` | Clean representative-point compare for BAPP preconditioning methods. |
| `debug_bapp_exp2_hotspot_blockage_sweep_sh` | active | 0.1.0 | utility | `scripts/debug/bapp_exp2_hotspot_blockage_sweep.sh` | BAPP Route-A Exp-2: |
| `debug_bapp_exp2_hotspot_pad_sweep_sh` | active | 0.1.0 | utility | `scripts/debug/bapp_exp2_hotspot_pad_sweep.sh` | BAPP Exp-2: |
| `debug_bapp_exp2_rudy_proxy_sweep_sh` | active | 0.1.0 | utility | `scripts/debug/bapp_exp2_rudy_proxy_sweep.sh` | BAPP Route-B proxy: |
| `debug_bapp_exp3_corridor_reservation_sh` | active | 0.1.0 | utility | `scripts/debug/bapp_exp3_corridor_reservation.sh` | BAPP Exp-3A: |
| `debug_bapp_replace_sink_density_exp1_sh` | active | 0.1.0 | place | `scripts/debug/bapp_replace_sink_density_exp1.sh` | BAPP Exp-1 (true RePlAce sink-density perturbation, low-cost). |
| `debug_bapp_sink_density_proxy_ab_sh` | active | 0.1.0 | utility | `scripts/debug/bapp_sink_density_proxy_ab.sh` | BAPP Exp-1 bridge experiment (low-cost): |
| `debug_bayes_opt_multilayer_htree_py` | active | 0.1.0 | utility | `scripts/debug/bayes_opt_multilayer_htree.py` | bayes opt multilayer htree |
| `debug_bound_sink_displacement_py` | active | 0.1.0 | place | `scripts/debug/bound_sink_displacement.py` | bound sink displacement |
| `debug_bridge_goal_settings_to_lastchance10_py` | active | 0.1.0 | utility | `scripts/debug/bridge_goal_settings_to_lastchance10.py` | bridge goal settings to lastchance10 |
| `debug_bscost_delay_consistency_capacity_gate_py` | active | 0.1.0 | utility | `scripts/debug/bscost_delay_consistency_capacity_gate.py` | bscost delay consistency capacity gate |
| `debug_bscost_theory_opt_stability_gate_py` | active | 0.1.0 | utility | `scripts/debug/bscost_theory_opt_stability_gate.py` | bscost theory opt stability gate |
| `debug_bucketed_delay_model_scorecard_py` | active | 0.1.0 | utility | `scripts/debug/bucketed_delay_model_scorecard.py` | bucketed delay model scorecard |
| `debug_build_backside_net_scorer_sh` | active | 0.1.0 | utility | `scripts/debug/build_backside_net_scorer.sh` | build backside net scorer |
| `debug_build_cout184_bm_detour_spec_py` | active | 0.1.0 | utility | `scripts/debug/build_cout184_bm_detour_spec.py` | build cout184 bm detour spec |
| `debug_build_openroad_route_spec_from_dump_py` | active | 0.1.0 | route | `scripts/debug/build_openroad_route_spec_from_dump.py` | build openroad route spec from dump |
| `debug_build_paired_delta_dataset_py` | active | 0.1.0 | utility | `scripts/debug/build_paired_delta_dataset.py` | build paired delta dataset |
| `debug_build_rc_aware_backside_features_py` | active | 0.1.0 | utility | `scripts/debug/build_rc_aware_backside_features.py` | build rc aware backside features |
| `debug_causal_single_net_backside_sweep_sh` | active | 0.1.0 | utility | `scripts/debug/causal_single_net_backside_sweep.sh` | Causal-style experiment: |
| `debug_check_delay_model_contract_py` | active | 0.1.0 | utility | `scripts/debug/check_delay_model_contract.py` | check delay model contract |
| `debug_check_lef_layer_compatibility_py` | active | 0.1.0 | utility | `scripts/debug/check_lef_layer_compatibility.py` | check lef layer compatibility |
| `debug_check_theory_veto_gate_py` | active | 0.1.0 | utility | `scripts/debug/check_theory_veto_gate.py` | check theory veto gate |
| `debug_circuit_expected_benefit_scorecard_py` | active | 0.1.0 | utility | `scripts/debug/circuit_expected_benefit_scorecard.py` | circuit expected benefit scorecard |
| `debug_clock_sink_density_heatmap_py` | active | 0.1.0 | cts | `scripts/debug/clock_sink_density_heatmap.py` | clock sink density heatmap |
| `debug_clocktree_cts_layer_compare_sh` | active | 0.1.0 | cts | `scripts/debug/clocktree_cts_layer_compare.sh` | Compare CTS route-layer policies while keeping signal routing frontside. |
| `debug_collect_replace_compare_master_report_py` | active | 0.1.0 | place | `scripts/debug/collect_replace_compare_master_report.py` | collect replace compare master report |
| `debug_collect_replace_route_ppa_compare_py` | active | 0.1.0 | place | `scripts/debug/collect_replace_route_ppa_compare.py` | collect replace route ppa compare |
| `debug_create_stage_golden_checkpoint_sh` | active | 0.1.0 | utility | `scripts/debug/create_stage_golden_checkpoint.sh` | create stage golden checkpoint |
| `debug_cts_precondition_ab_test_sh` | active | 0.1.0 | cts | `scripts/debug/cts_precondition_ab_test.sh` | Parallel A/B CTS preconditioning sweep. |
| `debug_cts_two_side_baseline_matrix_sh` | active | 0.1.0 | cts | `scripts/debug/cts_two_side_baseline_matrix.sh` | One-click matrix runner for CTS baselines: |
| `debug_def_to_stub_netlist_py` | active | 0.1.0 | utility | `scripts/debug/def_to_stub_netlist.py` | DEF uses backslash escapes for special characters in identifiers. |
| `debug_demo_cts_htree_0_baseline_route_sh` | active | 0.1.0 | cts | `scripts/debug/demo_cts_htree_0_baseline_route.sh` | Demo-0: |
| `debug_demo_cts_htree_1_fixed_tree_non_strict_sh` | active | 0.1.0 | cts | `scripts/debug/demo_cts_htree_1_fixed_tree_non_strict.sh` | Demo-1: |
| `debug_demo_cts_htree_2_fixed_tree_strict_sh` | active | 0.1.0 | cts | `scripts/debug/demo_cts_htree_2_fixed_tree_strict.sh` | Demo-2: |
| `debug_demo_multilayer_htree_cost_py` | active | 0.1.0 | utility | `scripts/debug/demo_multilayer_htree_cost.py` | demo multilayer htree cost |
| `debug_dp_select_from_scorer_report_py` | active | 0.1.0 | utility | `scripts/debug/dp_select_from_scorer_report.py` | dp select from scorer report |
| `debug_enforce_execution_contract_sh` | active | 0.1.0 | utility | `scripts/debug/enforce_execution_contract.sh` | enforce execution contract |
| `debug_estimate_s8_dynamic_expected_vs_actual_py` | active | 0.1.0 | utility | `scripts/debug/estimate_s8_dynamic_expected_vs_actual.py` | estimate s8 dynamic expected vs actual |
| `debug_estimate_s8_theoretical_vs_actual_power_py` | active | 0.1.0 | utility | `scripts/debug/estimate_s8_theoretical_vs_actual_power.py` | estimate s8 theoretical vs actual power |
| `debug_eval_h123_route_abc_gate_py` | active | 0.1.0 | route | `scripts/debug/eval_h123_route_abc_gate.py` | eval h123 route abc gate |
| `debug_evaluate_placement_resource_pressure_py` | active | 0.1.0 | place | `scripts/debug/evaluate_placement_resource_pressure.py` | evaluate placement resource pressure |
| `debug_extract_clock_buffer_instances_from_def_py` | active | 0.1.0 | cts | `scripts/debug/extract_clock_buffer_instances_from_def.py` | extract clock buffer instances from def |
| `debug_extract_clock_sink_instances_from_def_py` | active | 0.1.0 | cts | `scripts/debug/extract_clock_sink_instances_from_def.py` | extract clock sink instances from def |
| `debug_extract_initial_drv_wns_tns_py` | active | 0.1.0 | utility | `scripts/debug/extract_initial_drv_wns_tns.py` | extract initial drv wns tns |
| `debug_extract_topk_clock_nets_from_def_py` | active | 0.1.0 | cts | `scripts/debug/extract_topk_clock_nets_from_def.py` | extract topk clock nets from def |
| `debug_extract_topk_long_nets_from_def_py` | active | 0.1.0 | utility | `scripts/debug/extract_topk_long_nets_from_def.py` | extract topk long nets from def |
| `debug_finalize_openroad_cts_baseline_sh` | active | 0.1.0 | cts | `scripts/debug/finalize_openroad_cts_baseline.sh` | Finalize one OpenROAD-CTS baseline run from manifest generated by: |
| `debug_fit_rc_aware_sign_predictor_py` | active | 0.1.0 | utility | `scripts/debug/fit_rc_aware_sign_predictor.py` | fit rc aware sign predictor |
| `debug_gen_clock_corridor_blockages_py` | active | 0.1.0 | cts | `scripts/debug/gen_clock_corridor_blockages.py` | gen clock corridor blockages |
| `debug_gen_hotspot_soft_blockages_py` | active | 0.1.0 | utility | `scripts/debug/gen_hotspot_soft_blockages.py` | gen hotspot soft blockages |
| `debug_generate_bspdn_goal_campaign_py` | active | 0.1.0 | utility | `scripts/debug/generate_bspdn_goal_campaign.py` | generate bspdn goal campaign |
| `debug_generate_testcase_first_campaign_py` | active | 0.1.0 | utility | `scripts/debug/generate_testcase_first_campaign.py` | Few directions with high mechanism information gain. |
| `debug_gt3_backside_hypothesis_eval_sh` | active | 0.1.0 | utility | `scripts/debug/gt3_backside_hypothesis_eval.sh` | Evaluate hypothesis on PROBE GT3-like setup: |
| `debug_gt3_legalizer_lib_py` | active | 0.1.0 | utility | `scripts/debug/gt3_legalizer_lib.py` | gt3 legalizer lib |
| `debug_gt3_prects_legality_scorecard_py` | active | 0.1.0 | cts | `scripts/debug/gt3_prects_legality_scorecard.py` | gt3 prects legality scorecard |
| `debug_gt3_prects_legalizer_py` | active | 0.1.0 | cts | `scripts/debug/gt3_prects_legalizer.py` | gt3 prects legalizer |
| `debug_gt3_rc_completion_probe_sh` | active | 0.1.0 | utility | `scripts/debug/gt3_rc_completion_probe.sh` | GT3 RC-completion probe matrix. |
| `debug_launch_testcase_first_chipbench_campaign_py` | active | 0.1.0 | utility | `scripts/debug/launch_testcase_first_chipbench_campaign.py` | launch testcase first chipbench campaign |
| `debug_lc_compile_lib_to_db_sh` | active | 0.1.0 | utility | `scripts/debug/lc_compile_lib_to_db.sh` | Compile Liberty .lib into Synopsys .db using lc_shell on Slurm nodes. |
| `debug_manual_backside_patch_oracle_py` | active | 0.1.0 | utility | `scripts/debug/manual_backside_patch_oracle.py` | manual backside patch oracle |
| `debug_monitor_route_run_manifest_py` | active | 0.1.0 | route | `scripts/debug/monitor_route_run_manifest.py` | monitor route run manifest |
| `debug_offline_rc_consistency_regression_py` | active | 0.1.0 | utility | `scripts/debug/offline_rc_consistency_regression.py` | offline rc consistency regression |
| `debug_one_click_validate_new_cases_sh` | active | 0.1.0 | utility | `scripts/debug/one_click_validate_new_cases.sh` | One-click validation for new external RTL cases. |
| `scripts_debug_openroad_backside_rerouter_py` | active | 1.0.0 | route | `scripts/debug/openroad_backside_rerouter.py` | OpenROAD/OpenDB-backed local backside rerouting helper for selected nets |
| `debug_openroad_cts_bridge_baseline_all_cases_sh` | active | 0.1.0 | cts | `scripts/debug/openroad_cts_bridge_baseline_all_cases.sh` | Batch submit OpenROAD-CTS bridge baselines across multiple designs. |
| `debug_openroad_dump_net_wire_py` | active | 0.1.0 | utility | `scripts/debug/openroad_dump_net_wire.py` | openroad dump net wire |
| `debug_patch_def_from_bookshelf_pl_py` | active | 0.1.0 | utility | `scripts/debug/patch_def_from_bookshelf_pl.py` | patch def from bookshelf pl |
| `debug_pdk_flow_preflight_py` | active | 0.1.0 | preflight | `scripts/debug/pdk_flow_preflight.py` | pdk flow preflight |
| `debug_plot_backside_compare_py` | active | 0.1.0 | utility | `scripts/debug/plot_backside_compare.py` | plot backside compare |
| `debug_plot_net_cost_model_consistency_py` | active | 0.1.0 | utility | `scripts/debug/plot_net_cost_model_consistency.py` | plot net cost model consistency |
| `debug_postcts_dp_clock_signal_backside_sh` | active | 0.1.0 | cts | `scripts/debug/postcts_dp_clock_signal_backside.sh` | One-click experiment: |
| `debug_postcts_versiona_simple_backside_sh` | active | 0.1.0 | cts | `scripts/debug/postcts_versionA_simple_backside.sh` | Simple one-click Version-A demo: |
| `debug_postroute_backside_heuristic_oracle_py` | active | 0.1.0 | route | `scripts/debug/postroute_backside_heuristic_oracle.py` | postroute backside heuristic oracle |
| `debug_pre_experiment_reflection_py` | active | 0.1.0 | utility | `scripts/debug/pre_experiment_reflection.py` | pre experiment reflection |
| `debug_pre_route_model_search_py` | active | 0.1.0 | route | `scripts/debug/pre_route_model_search.py` | pre route model search |
| `debug_progress_monitor_py` | active | 0.1.0 | analysis | `scripts/debug/progress_monitor.py` | progress monitor |
| `debug_progress_monitor_sh` | active | 0.1.0 | analysis | `scripts/debug/progress_monitor.sh` | Background controller for scripts/debug/progress_monitor.py |
| `debug_propose_constrained_experiments_py` | active | 0.1.0 | utility | `scripts/debug/propose_constrained_experiments.py` | propose constrained experiments |
| `debug_quick_judge_replace_placement_py` | active | 0.1.0 | place | `scripts/debug/quick_judge_replace_placement.py` | quick judge replace placement |
| `debug_replace_clockdual_v1_round1_sweep_sh` | active | 0.1.0 | place | `scripts/debug/replace_clockdual_v1_round1_sweep.sh` | replace clockdual v1 round1 sweep |
| `debug_replace_ntuplace3_dp_bridge_sh` | active | 0.1.0 | place | `scripts/debug/replace_ntuplace3_dp_bridge.sh` | replace ntuplace3 dp bridge |
| `debug_route_postverify_shadow_scorer_py` | active | 0.1.0 | route | `scripts/debug/route_postverify_shadow_scorer.py` | route postverify shadow scorer |
| `debug_run_abcdplace_dp_py` | active | 0.1.0 | place | `scripts/debug/run_abcdplace_dp.py` | run abcdplace dp |
| `debug_run_autonomy_foundation_cycle_sh` | active | 0.1.0 | utility | `scripts/debug/run_autonomy_foundation_cycle.sh` | run autonomy foundation cycle |
| `debug_run_backside_crossover_phys_v2_multicase_sh` | active | 0.1.0 | utility | `scripts/debug/run_backside_crossover_phys_v2_multicase.sh` | format: |
| `debug_run_chipbench_highusage_route_batch_sh` | active | 0.1.0 | route | `scripts/debug/run_chipbench_highusage_route_batch.sh` | run chipbench highusage route batch |
| `debug_run_chipbench_replace_ab_cts_route_batch_sh` | active | 0.1.0 | place | `scripts/debug/run_chipbench_replace_ab_cts_route_batch.sh` | Optional override when DP_ENGINE=ntuplace3 (otherwise bridge script is used). |
| `debug_run_chipbench_replace_backside_usage_py` | active | 0.1.0 | place | `scripts/debug/run_chipbench_replace_backside_usage.py` | run chipbench replace backside usage |
| `debug_run_cts_htree_demo_phase1_sh` | active | 0.1.0 | cts | `scripts/debug/run_cts_htree_demo_phase1.sh` | Phase-1 CTS H-tree demo suite: |
| `debug_run_global_local_dualside_cts_sh` | active | 0.1.0 | cts | `scripts/debug/run_global_local_dualside_cts.sh` | Global+Local dual-side CTS experiment wrapper (single design). |
| `debug_run_offline_rc_consistency_regression_sh` | active | 0.1.0 | utility | `scripts/debug/run_offline_rc_consistency_regression.sh` | run offline rc consistency regression |
| `debug_run_plot_net_cost_model_consistency_sh` | active | 0.1.0 | utility | `scripts/debug/run_plot_net_cost_model_consistency.sh` | run plot net cost model consistency |
| `debug_run_pre_route_model_search_sh` | active | 0.1.0 | route | `scripts/debug/run_pre_route_model_search.sh` | run pre route model search |
| `debug_run_replace_costmodel_lastchance10_s8_sh` | active | 0.1.0 | place | `scripts/debug/run_replace_costmodel_lastchance10_s8.sh` | run replace costmodel lastchance10 s8 |
| `debug_run_replace_costmodel_vs_vanilla_route_ppa_sh` | active | 0.1.0 | place | `scripts/debug/run_replace_costmodel_vs_vanilla_route_ppa.sh` | run replace costmodel vs vanilla route ppa |
| `debug_run_replace_placement_ab_resource_gate_py` | active | 0.1.0 | place | `scripts/debug/run_replace_placement_ab_resource_gate.py` | run replace placement ab resource gate |
| `debug_run_route_abc_from_cts_golden_sh` | active | 0.1.0 | cts | `scripts/debug/run_route_abc_from_cts_golden.sh` | run route abc from cts golden |
| `scripts_debug_sanitize_def_for_openroad_py` | active | 1.0.0 | utility | `scripts/debug/sanitize_def_for_openroad.py` | Sanitize DEF naming/content so OpenROAD-side reroute utilities can consume it |
| `debug_screen_backside_delay_power_balance_py` | active | 0.1.0 | utility | `scripts/debug/screen_backside_delay_power_balance.py` | screen backside delay power balance |
| `debug_select_backside_nets_by_hot_congestion_py` | active | 0.1.0 | utility | `scripts/debug/select_backside_nets_by_hot_congestion.py` | select backside nets by hot congestion |
| `debug_select_backside_nets_cpp_sh` | active | 0.1.0 | utility | `scripts/debug/select_backside_nets_cpp.sh` | select backside nets cpp |
| `debug_select_backside_nets_power_first_py` | active | 0.1.0 | utility | `scripts/debug/select_backside_nets_power_first.py` | select backside nets power first |
| `debug_select_backside_nets_version_a_py` | active | 0.1.0 | utility | `scripts/debug/select_backside_nets_version_a.py` | select backside nets version a |
| `debug_select_hotspot_sink_subset_py` | active | 0.1.0 | utility | `scripts/debug/select_hotspot_sink_subset.py` | select hotspot sink subset |
| `debug_smoke_targeted_backside_route_toycase_sh` | active | 0.1.0 | route | `scripts/debug/smoke_targeted_backside_route_toycase.sh` | smoke targeted backside route toycase |
| `debug_split_class_reg_analysis_py` | active | 0.1.0 | utility | `scripts/debug/split_class_reg_analysis.py` | split class reg analysis |
| `debug_submit_backside_open_observe_sh` | active | 0.1.0 | utility | `scripts/debug/submit_backside_open_observe.sh` | Backside resource opening experiment (no targeted guidance). |
| `debug_submit_gt3_route_rc_consistency_sh` | active | 0.1.0 | route | `scripts/debug/submit_gt3_route_rc_consistency.sh` | submit gt3 route rc consistency |
| `debug_submit_large_cts_crash_repro_sh` | active | 0.1.0 | cts | `scripts/debug/submit_large_cts_crash_repro.sh` | Submit a large_design CTS run that reproduces the historical ccopt SEGV |
| `debug_submit_large_cts_stable_sh` | active | 0.1.0 | cts | `scripts/debug/submit_large_cts_stable.sh` | Submit a large_design CTS run with the validated stable CTS configuration |
| `debug_submit_large_prects_matrix_sh` | active | 0.1.0 | cts | `scripts/debug/submit_large_prects_matrix.sh` | Submit a pre-CTS experiment matrix on large_design to isolate runtime drivers. |
| `debug_submit_route_abc_from_cts_golden_sh` | active | 0.1.0 | cts | `scripts/debug/submit_route_abc_from_cts_golden.sh` | submit route abc from cts golden |
| `debug_summarize_ppa_unified_py` | active | 0.1.0 | utility | `scripts/debug/summarize_ppa_unified.py` | .../outputs/<design>/innovus/<runid> |
| `debug_sweep_multilayer_htree_weights_py` | active | 0.1.0 | utility | `scripts/debug/sweep_multilayer_htree_weights.py` | sweep multilayer htree weights |
| `debug_sweep_placement_resource_variants_py` | active | 0.1.0 | place | `scripts/debug/sweep_placement_resource_variants.py` | sweep placement resource variants |
| `debug_systematic_backside_model_analysis_py` | active | 0.1.0 | utility | `scripts/debug/systematic_backside_model_analysis.py` | systematic backside model analysis |
| `debug_systolic_backside_compare_sh` | active | 0.1.0 | utility | `scripts/debug/systolic_backside_compare.sh` | Compare backside-routing strategies on systolic_array_8x8. |
| `debug_systolic_clock_tree_backside_compare_sh` | active | 0.1.0 | cts | `scripts/debug/systolic_clock_tree_backside_compare.sh` | Compare clock-only backside routing strategies (signal nets unchanged). |
| `debug_systolic_cts_ppa_compare_sh` | active | 0.1.0 | cts | `scripts/debug/systolic_cts_ppa_compare.sh` | Fast CTS-only PPA comparison. |
| `debug_track_bspdn_goal_progress_py` | active | 0.1.0 | utility | `scripts/debug/track_bspdn_goal_progress.py` | track bspdn goal progress |
| `debug_validate_backside_delay_model_sh` | active | 0.1.0 | utility | `scripts/debug/validate_backside_delay_model.sh` | One-click validation: |
| `debug_validate_execution_contract_py` | active | 0.1.0 | utility | `scripts/debug/validate_execution_contract.py` | validate execution contract |
| `debug_visualize_large_disp_vs_ntsv_py` | active | 0.1.0 | utility | `scripts/debug/visualize_large_disp_vs_ntsv.py` | visualize large disp vs ntsv |
| `debug_visualize_postcts_drv_repair_py` | active | 0.1.0 | cts | `scripts/debug/visualize_postcts_drv_repair.py` | visualize postcts drv repair |
| `debug_visualize_replace_placement_clock_py` | active | 0.1.0 | place | `scripts/debug/visualize_replace_placement_clock.py` | COMPONENTS entries are typically one-line in this flow. |

## flow_orchestrator

| tool_id | lifecycle | version | stage | path | summary |
|---|---|---|---|---|---|
| `run_flow_sh` | active | 0.1.0 | utility | `scripts/run_flow.sh` | ============================================================ |
| `submit_flow_sh` | active | 0.1.0 | utility | `scripts/submit_flow.sh` | ============================================================ |

## flow_stage

| tool_id | lifecycle | version | stage | path | summary |
|---|---|---|---|---|---|
| `stages_dc_run_sh` | active | 0.1.0 | utility | `scripts/stages/dc/run.sh` | ============================================================ |
| `stages_eco_analysis_run_sh` | active | 0.1.0 | utility | `scripts/stages/eco_analysis/run.sh` | ============================================================ |
| `stages_innovus_run_sh` | active | 0.1.0 | utility | `scripts/stages/innovus/run.sh` | Usage: |
| `stages_innovus_eco_run_sh` | active | 0.1.0 | utility | `scripts/stages/innovus_eco/run.sh` | ============================================================ |
| `stages_primetime_postdc_run_sh` | active | 0.1.0 | utility | `scripts/stages/primetime_postdc/run.sh` | ============================================================ |
| `stages_primetime_postpnr_run_sh` | active | 0.1.0 | utility | `scripts/stages/primetime_postpnr/run.sh` | ============================================================ |

## flow_stage_aux

| tool_id | lifecycle | version | stage | path | summary |
|---|---|---|---|---|---|
| `stages_dc_readme_md` | active | 0.1.0 | utility | `scripts/stages/dc/README.md` | Design Compiler (Synthesis) |
| `stages_dc_interface_yaml` | active | 0.1.0 | utility | `scripts/stages/dc/interface.yaml` | interface |
| `stages_eco_analysis_readme_md` | active | 0.1.0 | utility | `scripts/stages/eco_analysis/README.md` | ECO (Engineering Change Order) Flow |
| `stages_eco_analysis_analyze_timing_py` | active | 0.1.0 | analysis | `scripts/stages/eco_analysis/analyze_timing.py` | Extract setup timing |
| `stages_innovus_readme_md` | active | 0.1.0 | utility | `scripts/stages/innovus/README.md` | Innovus Place & Route Stage |
| `stages_innovus_interface_yaml` | active | 0.1.0 | utility | `scripts/stages/innovus/interface.yaml` | interface |
| `stages_innovus_run_openroad_cts_bridge_sh` | active | 0.1.0 | cts | `scripts/stages/innovus/run_openroad_cts_bridge.sh` | One-click bridge: |
| `stages_innovus_eco_readme_md` | active | 0.1.0 | utility | `scripts/stages/innovus_eco/README.md` | Innovus ECO Stage |
| `stages_primetime_postdc_readme_md` | active | 0.1.0 | utility | `scripts/stages/primetime_postdc/README.md` | PrimeTime Post-DC STA Stage |
| `stages_primetime_postdc_interface_yaml` | active | 0.1.0 | utility | `scripts/stages/primetime_postdc/interface.yaml` | interface |
| `stages_primetime_postpnr_readme_md` | active | 0.1.0 | utility | `scripts/stages/primetime_postpnr/README.md` | PrimeTime Post-PnR STA Stage |
| `stages_primetime_postpnr_debug_sh` | active | 0.1.0 | utility | `scripts/stages/primetime_postpnr/debug.sh` | ============================================================ |
| `stages_primetime_postpnr_debug_tcl` | active | 0.1.0 | utility | `scripts/stages/primetime_postpnr/debug.tcl` | ============================================================ |
| `stages_primetime_postpnr_interface_yaml` | active | 0.1.0 | utility | `scripts/stages/primetime_postpnr/interface.yaml` | interface |

## flow_stage_tcl

| tool_id | lifecycle | version | stage | path | summary |
|---|---|---|---|---|---|
| `stages_dc_run_tcl` | active | 0.1.0 | utility | `scripts/stages/dc/run.tcl` | ============================================================ |
| `stages_innovus_run_tcl` | active | 0.1.0 | utility | `scripts/stages/innovus/run.tcl` | ============================================================ |
| `stages_innovus_eco_run_tcl` | active | 0.1.0 | utility | `scripts/stages/innovus_eco/run.tcl` | ============================================================ |
| `stages_primetime_postdc_run_tcl` | active | 0.1.0 | utility | `scripts/stages/primetime_postdc/run.tcl` | ============================================================ |
| `stages_primetime_postpnr_run_tcl` | active | 0.1.0 | utility | `scripts/stages/primetime_postpnr/run.tcl` | ============================================================ |

## script

| tool_id | lifecycle | version | stage | path | summary |
|---|---|---|---|---|---|
| `clean_sh` | active | 0.1.0 | utility | `scripts/clean.sh` | ============================================================ |
| `env_cadence_innovus_sh` | active | 0.1.0 | utility | `scripts/env/cadence_innovus.sh` | ============================================================ |
| `env_synopsys_dc_sh` | active | 0.1.0 | utility | `scripts/env/synopsys_dc.sh` | Synopsys Design Compiler environment |
| `env_synopsys_primetime_sh` | active | 0.1.0 | utility | `scripts/env/synopsys_primetime.sh` | ============================================================ |
| `env_test_smtp_py` | active | 0.1.0 | utility | `scripts/env/test_smtp.py` | test smtp |
| `find_tool_sh` | active | 0.1.0 | utility | `scripts/find_tool.sh` | find tool |
| `switch_readme_lang_sh` | active | 0.1.0 | utility | `scripts/switch_readme_lang.sh` | Switch README language by copying README_zh.md or README_en.md into README.md |

## tech_utility

| tool_id | lifecycle | version | stage | path | summary |
|---|---|---|---|---|---|
| `tech_asap7_sh` | active | 0.1.0 | utility | `scripts/tech/asap7.sh` | ============================================================ |
| `tech_extend_probe_gt3_backside_techlef_py` | active | 0.1.0 | utility | `scripts/tech/extend_probe_gt3_backside_techlef.py` | extend probe gt3 backside techlef |
| `tech_freepdk3_sh` | active | 0.1.0 | utility | `scripts/tech/freepdk3.sh` | ============================================================ |
| `tech_gt3_sh` | active | 0.1.0 | utility | `scripts/tech/gt3.sh` | ============================================================ |
| `tech_prepare_freepdk3_proxy_sh` | active | 0.1.0 | utility | `scripts/tech/prepare_freepdk3_proxy.sh` | ============================================================ |
| `tech_prepare_gt3_sh` | active | 0.1.0 | utility | `scripts/tech/prepare_gt3.sh` | ============================================================ |
| `tech_prepare_gt3_fixed_sh` | active | 0.1.0 | utility | `scripts/tech/prepare_gt3_fixed.sh` | ============================================================ |
| `tech_prepare_probe_gt3_sh` | active | 0.1.0 | utility | `scripts/tech/prepare_probe_gt3.sh` | Prepare a local PROBE GT3 tech bundle under tech/PROBE_GT3. |
| `tech_probe_gt3_sh` | active | 0.1.0 | utility | `scripts/tech/probe_gt3.sh` | ============================================================ |

