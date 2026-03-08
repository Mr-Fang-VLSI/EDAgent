# Knowledge Base

This folder is the operational knowledge hub for this project.

Goal:
- make decisions traceable,
- make execution reproducible,
- avoid repeating known mistakes.

## Retrieval entrypoint
Use unified local retrieval when planning experiments or theory updates:

```bash
python3 scripts/common/unified_kb_query.py build
python3 scripts/common/unified_kb_query.py query --source all --mode hybrid --query "backside placement cts legalization"
```

This searches both `docs/knowledge_base` and `docs/papers/index/paper_index.json` and writes ranked results to `docs/knowledge_base/index/query_last.tsv`.

## Landscape fusion
To maintain logical links between paper knowledge and research decisions, keep both landscapes updated whenever new summaries are added:

```bash
python3 scripts/common/paper_landscape_sync.py build
```

Outputs:
- `docs/knowledge_base/95_PROBLEM_LANDSCAPE.md`
- `docs/knowledge_base/96_METHOD_LANDSCAPE.md`
- `docs/knowledge_base/index/landscape_graph.json`
- `docs/knowledge_base/index/landscape_problem_method_matrix.tsv`

## Required Usage Rule
Before running any new experiment batch, read:
1. `docs/knowledge_base/00_START_HERE.md`
2. `docs/knowledge_base/10_TASK_EXECUTION_PROTOCOL.md`
3. `docs/knowledge_base/11_INTERACTION_CHECKLIST.md`
4. at least one domain doc related to the task (`20/30/40` series)

If this is skipped, the run is considered non-baseline and should not be used as evidence.

## Structure
- `00_START_HERE.md`: fast entry and mandatory read map.
- `10_TASK_EXECUTION_PROTOCOL.md`: pre-run checklist and execution protocol.
- `11_INTERACTION_CHECKLIST.md`: per-interaction start/end maintenance checklist.
- `20_LAYER_POLICY_CTS_PDN_BACKSIDE.md`: layer assignment policy for CTS/PDN/backside.
- `30_BACKSIDE_VIA_CONNECTIVITY_CHECKLIST.md`: BM1/BM2/nTSV connectivity checks.
- `40_FLOW_CHANGE_ROADMAP.md`: near-term flow change plan and verification matrix.
- `50_OFFLINE_RC_REGRESSION_GOLDEN.md`: offline regression and golden governance for delay-model consistency.
- `60_NET_COST_MODEL_VS_HPWL_STATUS_20260304.md`: consolidated status of current net-cost model vs HPWL, including strengths/gaps/next steps.
- `70_STAGE_CHECKPOINT_GOLDEN_WORKFLOW_20260304.md`: immutable stage checkpoint workflow (`place/cts/route`) for fast resume experiments.
- `80_BSCOST_THREE_SKILL_WORKFLOW_20260304.md`: three-skill workflow for backside cost-model upgrade and stability-gated promotion.
- `82_BACKSIDE_SHORT_NET_DIAGNOSIS_AND_JUDGMENT_MODEL_20260304.md`: why backside short nets appear and why a judgment model is required beyond `min(front,back)`.
- `83_REPLACE_DUALSIDE_OBJECTIVE_UPGRADE_PLAN_20260304.md`: RePlAce dual-side objective upgrade plan (signal-first + capacity-aware), with gate-driven validation and PPA-case target.
- `84_REPLACE_COMPARISON_POLICY_20260304.md`: hard benchmarking policy (algorithm claims must be Vanilla RePlAce vs modified RePlAce; Innovus is downstream validation only).
- `85_SKILL_SYSTEM_INTEGRATION_20260304.md`: skill-system integration history; latest governance entry is `AGENTS.md` (root), with direct routing through `workflow-router` and no compatibility entry skill.
- `86_PAPER_EVIDENCE_LIBRARY_AND_RETRIEVAL_20260304.md`: paper storage/retrieval architecture for semantic + keyword + logic search.
- `88_PDF_PARSING_PIPELINE_GROBID_FIRST_20260304.md`: default local paper parsing pipeline (GROBID-first + fallback) and artifact contract.
- `90_HYPOTHESIS_VALIDATION_LOG.md`: running log of hypothesis, validation experiment, evidence, and conclusion.
- `91_AUTONOMY_FOUNDATION_STACK_20260305.md`: hard-gated autonomy foundation (unified preflight, execution contract, memory DB, constrained proposal).
- `92_INFRASTRUCTURE_STEWARDSHIP_20260306.md`: contract for use/maintain/develop modes of agent + KB + tool registry + skills infrastructure.
- `93_EDA_RESEARCH_FULL_CHAIN_20260306.md`: end-to-end research chain (knowledge -> papers -> idea debate -> hypothesis -> implementation -> versioning -> validation -> retro).
- `94_BSPDN_GOAL_MILESTONE_PLAN_20260306.md`: staged milestone plan toward target BSPDN power/timing goals.
- `95_PROBLEM_LANDSCAPE.md`: auto-synced problem landscape from paper summaries with cross-paper bottleneck clustering.
- `96_METHOD_LANDSCAPE.md`: auto-synced method landscape with problem-method link structure.
- `97_GLOBAL_RESEARCH_LANDSCAPE.md`: global paper-level map (`subproblem -> method -> effect -> group -> paper`) with curation hooks.
- `98_LITERATURE_FEEDBACK_LOOP.md`: auto-generated feedback report for missing directions and stale methods with targeted retrieval queue.
- `99_AUTOIDEA_FUSION_REPORT_20260306.md`: bridge report that fuses autoIdea recommendation/idea outputs into local governed workflow.
- `100_AGENT_SKILL_STANDALONE_PACKAGING_20260306.md`: standalone packaging workflow for exporting `agent+skills` into an independent repo-ready bundle.
- `101_CTS_CONVERGENCE_ROOTCAUSE_SOP_20260306.md`: mandatory root-cause workflow for diagnosing CTS/route non-convergence before changing optimization knobs.
- `102_DEVELOPMENT_PROMOTION_AND_PRINCIPLE_CAPTURE_SOP_20260307.md`: development-authority vs release-mirror policy, plus the rule that user-stated durable principles must be persisted into KB/protocol/SOP.
- `103_SKILL_SYSTEM_UPGRADE_RETRO_AND_VALIDATION_PLAN_20260307.md`: retrospective for the recent skill-system upgrade, including expected benefits, falsification signals, and a later validation plan.
- `104_EXPERIMENT_EXPERIENCE_LAYER_AND_PHENOMENOLOGY_WORKFLOW_20260307.md`: horizontal `log -> result -> conclusion -> experience` extraction model and how execution, retro, and theory-veto consume it.
- `105_SCRIPT_PATTERN_MEMORY_AND_CURATION_WORKFLOW_20260307.md`: horizontal script-writing experience model for wrapper/runtime/abstraction lessons and when to promote them into reusable guidance.
- `106_SKILL_ADOPTION_MONITORING_WORKFLOW_20260307.md`: monitor whether newly introduced skills actually enter use and help maintainability over time.
- `107_BSPDN_TOPOLOGY_AND_BENEFIT_VALIDATION_PROGRAM_20260307.md`: mechanism-first validation program linking PDK topology audit, PDN sufficiency, benefit attribution, and later backside-aware placement promotion.
- `108_LONG_LOG_ROLLUP_AND_PRINCIPLE_EXTRACTION_WORKFLOW_20260307.md`: periodic compression workflow for turning long append-only maintenance logs into dense experience/principle rollups.
- `109_SKILL_NAMING_AND_GROUPING_POLICY_20260307.md`: policy for making skill names or directory placement reveal both function and architectural level/family.
- `110_CURRENT_AGENT_SKILL_STRUCTURE_REPORT_20260307.md`: structural snapshot of the current skill system after the middle-layer rename cleanup, including layer counts, dependency shape, strengths, and pressure points.
- `111_ROUTING_ORCHESTRATION_OWNER_CONTRACT_20260307.md`: canonical short contract that separates routing, workflow ownership, and bounded execution orchestration.
- `112_PAPER_LEARNING_AND_EXPERT_REFRESH_FLOW_20260307.md`: canonical flow for unified paper nomination, human download queues, summary ingestion, learning-round synthesis, research-guidance closeout, and expert-skill refresh.
- `113_BACKSIDE_ROUTING_REALIZATION_EXPERT_WORKFLOW_20260307.md`: expert workflow boundary for backside route realization, local rerouter bring-up, and the bridge from theory-ranked nets to physically realized `BM1/BM2` routing.
- `114_CONDA_PROJECT_ENVIRONMENT_MANAGEMENT_WORKFLOW_20260307.md`: canonical project-level conda environment management contract for env discovery, package availability checks, and explicit `conda run -n ...` usage.
- `107_BSPDN_TOPOLOGY_AND_BENEFIT_VALIDATION_PROGRAM_20260307.md`: now also names the preferred expert skills for topology validity, PDN sufficiency, and benefit attribution gates.
- `templates/task_brief_template.md`: copy this to create a run brief before execution.
- `templates/research_chain_task_brief_template.md`: task-brief template for full-chain research.
- `templates/idea_debate_note_template.md`: standardized brainstorm/debate note format.
- `templates/hypothesis_experiment_matrix_template.tsv`: hypothesis-to-experiment matrix template.
- `templates/experiment_results_template.tsv`: default structured results skeleton for experiment phenomenology extraction.
- `templates/experiment_conclusion_template.md`: default batch-local mechanism conclusion skeleton.
- `templates/experiment_experience_delta_template.md`: default reusable experiment-experience delta skeleton.
- `templates/script_incident_template.md`: default script incident capture skeleton.
- `templates/script_pattern_note_template.md`: default reusable script pattern / anti-pattern note skeleton.
- `templates/maintenance_log_rollup_template.md`: default dense rollup skeleton for long append-only logs.
- `templates/paper_learning_round_synthesis_template.md`: default dense synthesis skeleton for one completed learning round.
- `templates/paper_learning_next_step_guidance_template.md`: default bridge note from learning-round results to concrete next-step research guidance.

## Relation to Existing Docs
This folder does not replace topic docs in:
- `docs/pdk_tech/`
- `docs/cts_algorithms/`
- `docs/flow_reliability/`
- `docs/backside_routing/`

It organizes how to use them consistently before action.
