# 00 Start Here

This is the required entry point before any task execution.

## Step 1: Identify task type
Choose one:
- A) PDK / RC / via modeling
- B) CTS algorithm / layer policy
- C) flow stability / job orchestration
- D) delay-model consistency validation
- E) end-to-end research chain (knowledge -> papers -> idea -> hypothesis -> implementation -> validation)

## Step 2: Mandatory documents by task type
- A) Read:
  - `docs/pdk_tech/gt3_ntsv_research_baseline_20260303.md`
  - `docs/pdk_tech/gt3_backside_parameter_traceability_20260301.md`
  - `docs/knowledge_base/30_BACKSIDE_VIA_CONNECTIVITY_CHECKLIST.md`
- B) Read:
  - `docs/cts_algorithms/backside_cost_model_principled_v2_20260303.md`
  - `docs/cts_algorithms/openroad_replace_clock_softmin_dualpath_plan_20260303.md`
  - `docs/knowledge_base/20_LAYER_POLICY_CTS_PDN_BACKSIDE.md`
- C) Read:
  - `docs/flow_reliability/cts_crash_rca_and_playbook.md`
  - `docs/flow_reliability/large_design_open_issues_tracker.md`
  - `docs/knowledge_base/10_TASK_EXECUTION_PROTOCOL.md`
  - `docs/knowledge_base/101_CTS_CONVERGENCE_ROOTCAUSE_SOP_20260306.md`
- D) Read:
  - `docs/knowledge_base/20_LAYER_POLICY_CTS_PDN_BACKSIDE.md`
  - `docs/knowledge_base/30_BACKSIDE_VIA_CONNECTIVITY_CHECKLIST.md`
  - `docs/knowledge_base/40_FLOW_CHANGE_ROADMAP.md`
  - `docs/knowledge_base/60_NET_COST_MODEL_VS_HPWL_STATUS_20260304.md`
  - `docs/knowledge_base/70_STAGE_CHECKPOINT_GOLDEN_WORKFLOW_20260304.md`
  - `docs/knowledge_base/80_BSCOST_THREE_SKILL_WORKFLOW_20260304.md`
  - `docs/knowledge_base/82_BACKSIDE_SHORT_NET_DIAGNOSIS_AND_JUDGMENT_MODEL_20260304.md`
  - `docs/knowledge_base/83_REPLACE_DUALSIDE_OBJECTIVE_UPGRADE_PLAN_20260304.md`
  - `docs/knowledge_base/84_REPLACE_COMPARISON_POLICY_20260304.md`
  - `docs/knowledge_base/85_SKILL_SYSTEM_INTEGRATION_20260304.md`
  - `docs/knowledge_base/86_PAPER_EVIDENCE_LIBRARY_AND_RETRIEVAL_20260304.md`
  - `docs/knowledge_base/88_PDF_PARSING_PIPELINE_GROBID_FIRST_20260304.md`
  - `docs/knowledge_base/91_AUTONOMY_FOUNDATION_STACK_20260305.md`
- E) Read:
  - `docs/knowledge_base/85_SKILL_SYSTEM_INTEGRATION_20260304.md`
  - `docs/knowledge_base/92_INFRASTRUCTURE_STEWARDSHIP_20260306.md`
  - `docs/knowledge_base/102_DEVELOPMENT_PROMOTION_AND_PRINCIPLE_CAPTURE_SOP_20260307.md`
  - `docs/knowledge_base/93_EDA_RESEARCH_FULL_CHAIN_20260306.md`
  - `docs/knowledge_base/94_BSPDN_GOAL_MILESTONE_PLAN_20260306.md`
  - `docs/knowledge_base/95_PROBLEM_LANDSCAPE.md`
  - `docs/knowledge_base/96_METHOD_LANDSCAPE.md`
  - `docs/knowledge_base/97_GLOBAL_RESEARCH_LANDSCAPE.md`
  - `docs/knowledge_base/98_LITERATURE_FEEDBACK_LOOP.md`
  - `docs/knowledge_base/99_AUTOIDEA_FUSION_REPORT_20260306.md`
  - `docs/knowledge_base/100_AGENT_SKILL_STANDALONE_PACKAGING_20260306.md`
  - `docs/knowledge_base/86_PAPER_EVIDENCE_LIBRARY_AND_RETRIEVAL_20260304.md`
  - `docs/knowledge_base/88_PDF_PARSING_PIPELINE_GROBID_FIRST_20260304.md`

## Step 3: Create task brief
Copy:
- `docs/knowledge_base/templates/task_brief_template.md`

Create a new file under:
- `slurm_logs/04_delay_modeling/` or matching experiment folder

Do not submit jobs until the brief is filled.

## Step 3.2: Complete interaction checklist
Read and execute:
- `docs/knowledge_base/11_INTERACTION_CHECKLIST.md`

## Step 3.3: Tri-source evidence lock (mandatory)
Before any new submission/conclusion, confirm all three:
- local data/log evidence,
- local knowledge-base references,
- internet/primary-source evidence (when assumptions can drift).

## Step 3.5: Search existing tools first
Run:
- `python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>`

If suitable script exists, reuse it. Add a short note in task brief.

## Step 4: Run and record
Every run must record:
- run tag
- exact wrapper/script path
- key knobs
- expected success criterion
- pass/fail reason
- hypothesis and validation status in:
  - `docs/knowledge_base/90_HYPOTHESIS_VALIDATION_LOG.md`

## Current critical context
- We have evidence that backside-open flow can run but backside utilization is low.
- We have a concrete warning:
  - `IMPSR-379: missing VIAGEN rules on layer BM1`
  - seen in `slurm_logs/gt3_route_rc_consistency_research_bsntsv_flowopen_20260303_230308_back_313239.out`
- This warning can directly limit backside routability and must be addressed before drawing strong conclusions.

## Persistent governance note
- current repo = development authority
- `exports/eda_agent_skill_system` = release mirror
- principle/policy changes should be documented in the current repo first
- do not auto-promote those changes to the export/public mirror without explicit user intent
