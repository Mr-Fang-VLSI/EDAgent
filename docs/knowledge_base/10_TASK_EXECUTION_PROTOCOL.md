# 10 Task Execution Protocol

This protocol is mandatory for experiment credibility.

## Pre-run checklist
Mark all items before submission:

- [ ] Task brief file created from template.
- [ ] Relevant knowledge docs were read and linked in the brief.
- [ ] Tri-source evidence is prepared:
  - local run data/logs,
  - local knowledge base references,
  - internet/primary-source references (for assumptions likely to drift).
- [ ] `docs/knowledge_base/11_INTERACTION_CHECKLIST.md` start section completed.
- [ ] Tool registry searched to avoid duplicate scripts.
- [ ] For packaged testcase flows, `check_design_package.py --require-design-top-match` passed.
- [ ] Tech profile and techlef source are explicit.
- [ ] Run objective and success metric are explicit.
- [ ] Compare baseline is explicit.
- [ ] Claim class is explicit: `A_algorithmic` or `B_realizability`.
- [ ] If `A_algorithmic`: baseline is `vanilla_replace` (not Innovus).
- [ ] If Innovus is used: mark it as secondary realizability validation only.
- [ ] If `A_algorithmic` + downstream Innovus validation: lock route policy identical across variants (default `--open-backside-route` for both).
- [ ] Monitor path is defined.
- [ ] Manifest path is defined.
- [ ] Monitor file is created at submission time, not deferred.
- [ ] Job IDs will be reported to the user immediately after submission.
- [ ] If ETA will be reported, its estimation basis is defined.
- [ ] Stop criteria are defined.

## Submission rules
- Prefer one controller script per experiment family.
- Keep run tags unique and descriptive.
- Use immutable tech staging for concurrent jobs whenever possible.
- Every experiment submission must create a canonical monitor artifact at submit time.
- Prefer the reusable monitor stack instead of hand-written monitor markdown:
  - `python3.11 scripts/debug/progress_monitor.py --manifest <manifest.tsv> --out-prefix <monitor_prefix>`
  - or `bash scripts/debug/progress_monitor.sh start --manifest <manifest.tsv> --out-prefix <monitor_prefix> --exit-when-complete`
- The same turn that reports job submission must also report the monitor file path to the user.
- Manual Slurm submissions must use canonical CPU defaults unless there is a documented reason not to:
  - partition: `cpu-research`
  - qos: `olympus-cpu-research`
  - account: `all`
  - preferred helper: `scripts/common/sbatch_cpu_research.sh`
- Do not mix "force routing" and "open routing" in the same conclusion batch.
- If new script is needed, record why existing catalog entries are insufficient.
- For route/cts submissions, generate unified preflight report first (`pdk_flow_preflight.py`) and block on FAIL.
- For new BSPDN layer-role or topology claims, complete a topology-validity gate first:
  - produce `hypothesis_experiment_matrix.tsv`, `experiment_design_note.md`, and `promotion_gate.md`,
  - make the current `BPR / BM1 / BM2 / M0 / M1 / nTSV` assumptions explicit,
  - block large comparison batches if the topology gate is `NO-GO`.
- For testcase-backed DC/Innovus submissions, block on testcase package check FAIL:

```bash
python3 scripts/common/check_design_package.py --design <design> --require-design-top-match --out-md <report.md>
```

- For end-to-end research-chain tasks, initialize chain workspace first (`init_research_chain.py`) and keep stage artifacts updated.
- After submission, report monitor/manifest/job-id information to the user in the same interaction turn.

## Result collection rules
Each batch summary must include:
- stage reached (`place`, `cts`, `route`, `extract`)
- WNS/TNS/violating paths
- DRV first snapshot and final snapshot
- layer usage summary (front vs backside)
- runtime
- failure signature if failed
- execution-contract verdict and fail rows (`validate_execution_contract.py`)
- if optimization continues: memory/proposal artifacts (`experiment_memory.py`, `propose_constrained_experiments.py`)
- one explicit hypothesis-validation-conclusion block:
  - hypothesis,
  - experiment setup,
  - measured outcome,
  - conclusion (supported / partially supported / rejected).

When the batch exposed reusable behavior, also lift evidence through four explicit layers:
1. `log`: raw stdout/stderr/reports/monitor/manifest
2. `result`: structured extracted facts (`WNS/TNS/PPA/runtime/backside usage/gate status`)
3. `conclusion`: batch-local mechanism judgment
4. `experience`: cross-batch reusable recommendation or veto-relevant pattern

Do not skip directly from raw logs to durable advice without writing at least `result` and `conclusion`.

Default skeletons:
- `docs/knowledge_base/templates/experiment_results_template.tsv`
- `docs/knowledge_base/templates/experiment_conclusion_template.md`
- `docs/knowledge_base/templates/experiment_experience_delta_template.md`

## Convergence root-cause protocol
Use this when CTS/route convergence is unstable or runtime is being wasted by repeated legality churn.

1. Separate `mechanism diagnosis` from `optimization`.
2. Do not launch multi-knob rescue experiments before a single-variable diagnostic is defined.
3. First isolate whether the dominant issue is:
   - placement legality,
   - PDK/row-track/pin-access mismatch,
   - internal tool-stage behavior (for example ccopt internal refine place),
   - or a mixed mechanism.
4. Hold the resume DEF fixed whenever possible and vary only one control at a time.
5. Record both:
   - first appearance point of failure signatures (`IMPCCOPT-2030`, `IMPSP-2020`, `IMPSP-2031`, `IMPSP-2042`),
   - cumulative counts of signature classes (`Orientation_Violation`, `DRC_Violation`, `Soft_Blockage_Violation`).
6. Distinguish `entry-clean` from `stage-stable`:
   - `checkPlace_before = OK` only proves entry cleanliness,
   - it does not prove ccopt/route-stage legality stability.
7. If two variants reach different depths, do not compare raw error totals without stating the depth difference.
8. If an internal tool stage appears to dominate behavior, redirect the next A/B to isolate that stage rather than adding new placement heuristics.
9. When evidence is sufficient to identify a low-value branch, stop those jobs and recycle compute to a tighter diagnostic.

## Interaction maintenance rule (always-on)
For each interaction turn:
- run start checklist from `11_INTERACTION_CHECKLIST.md`,
- run end checklist from `11_INTERACTION_CHECKLIST.md`,
- update maintenance log in `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`.

## Principle capture rule
If the user explicitly states a durable principle, preference, governance rule, or workflow rule, agent must treat it as persistable guidance rather than ephemeral chat context.

Default action:
1. formalize it into KB/protocol/SOP,
2. update the appropriate owning document,
3. record the change in maintenance log,
4. use the documented rule in later turns.

Unless the user explicitly requests release promotion, such principle-driven changes should update the current repo only, not the exported/public EDAgent mirror.

## Conclusion rules
- If known tech warnings exist (for example missing VIAGEN), conclusions must be marked `provisional`.
- If baseline and variant differ in more than one major knob, no causal claim is allowed.
- If the same attractor appears, report it explicitly and avoid overfitting interpretation.
- If internet evidence was required but missing, the conclusion must be marked `evidence-incomplete`.
- If claim class is `A_algorithmic` and primary baseline is not `vanilla_replace`, conclusion must be marked `INVALID_COMPARISON_POLICY`.
- For research-chain conclusions, run `research_chain_guard.py`; if any critical stage artifact is missing, conclusion must be marked `CHAIN_INCOMPLETE`.
- If a later theory-veto or retrospective relies on repeated empirical experience, the cited experience item must link back to concrete `result` and `conclusion` artifacts rather than only free-form narrative.
