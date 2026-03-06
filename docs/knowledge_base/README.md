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
- `85_SKILL_SYSTEM_INTEGRATION_20260304.md`: skill-system integration history; latest governance entry is `agent.md` (root), with `eda-chief` as compatibility shim.
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
- `templates/task_brief_template.md`: copy this to create a run brief before execution.
- `templates/research_chain_task_brief_template.md`: task-brief template for full-chain research.
- `templates/idea_debate_note_template.md`: standardized brainstorm/debate note format.
- `templates/hypothesis_experiment_matrix_template.tsv`: hypothesis-to-experiment matrix template.

## Relation to Existing Docs
This folder does not replace topic docs in:
- `docs/pdk_tech/`
- `docs/cts_algorithms/`
- `docs/flow_reliability/`
- `docs/backside_routing/`

It organizes how to use them consistently before action.
