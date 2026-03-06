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
- [ ] Tech profile and techlef source are explicit.
- [ ] Run objective and success metric are explicit.
- [ ] Compare baseline is explicit.
- [ ] Claim class is explicit: `A_algorithmic` or `B_realizability`.
- [ ] If `A_algorithmic`: baseline is `vanilla_replace` (not Innovus).
- [ ] If Innovus is used: mark it as secondary realizability validation only.
- [ ] If `A_algorithmic` + downstream Innovus validation: lock route policy identical across variants (default `--open-backside-route` for both).
- [ ] Monitor path is defined.
- [ ] Stop criteria are defined.

## Submission rules
- Prefer one controller script per experiment family.
- Keep run tags unique and descriptive.
- Use immutable tech staging for concurrent jobs whenever possible.
- Do not mix "force routing" and "open routing" in the same conclusion batch.
- If new script is needed, record why existing catalog entries are insufficient.
- For route/cts submissions, generate unified preflight report first (`pdk_flow_preflight.py`) and block on FAIL.
- For end-to-end research-chain tasks, initialize chain workspace first (`init_research_chain.py`) and keep stage artifacts updated.

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

## Interaction maintenance rule (always-on)
For each interaction turn:
- run start checklist from `11_INTERACTION_CHECKLIST.md`,
- run end checklist from `11_INTERACTION_CHECKLIST.md`,
- update maintenance log in `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`.

## Conclusion rules
- If known tech warnings exist (for example missing VIAGEN), conclusions must be marked `provisional`.
- If baseline and variant differ in more than one major knob, no causal claim is allowed.
- If the same attractor appears, report it explicitly and avoid overfitting interpretation.
- If internet evidence was required but missing, the conclusion must be marked `evidence-incomplete`.
- If claim class is `A_algorithmic` and primary baseline is not `vanilla_replace`, conclusion must be marked `INVALID_COMPARISON_POLICY`.
- For research-chain conclusions, run `research_chain_guard.py`; if any critical stage artifact is missing, conclusion must be marked `CHAIN_INCOMPLETE`.
