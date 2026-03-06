# 11 Interaction Checklist (Mandatory)

This checklist is executed **for every interaction**.

Scope:
- Knowledge Base (`docs/knowledge_base/`)
- Tool Registry (`docs/tool_registry/`)

---

## A. Start-of-Interaction Checklist

Complete these before making changes or launching jobs:

- [ ] Confirm task type and objective in 1-2 lines.
- [ ] Declare `claim_class` (`A_algorithmic` vs `B_realizability`) and intended baseline.
- [ ] Read `docs/knowledge_base/00_START_HERE.md`.
- [ ] Read `docs/knowledge_base/10_TASK_EXECUTION_PROTOCOL.md`.
- [ ] Prepare tri-source evidence set:
  - local data/logs to analyze,
  - relevant local KB docs,
  - internet/primary-source references (if assumptions may drift).
- [ ] Search existing tools first:
  - `python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>`
  - or `bash scripts/find_tool.sh <keyword1> <keyword2>`
- [ ] Decide reuse vs new script:
  - if reuse: record chosen script path.
  - if new: record why existing tools are insufficient.
- [ ] Comparison-policy check:
  - if `A_algorithmic`, primary baseline must be `vanilla_replace`.
  - if Innovus is involved, keep it as secondary realizability evidence.
  - if downstream Innovus validation is included, lock route policy identically across variants (default `--open-backside-route` for both).
- [ ] If route/cts will be submitted, run unified preflight and save report path.
- [ ] If this is a full research-chain task, initialize workspace:
  - `python3 scripts/common/init_research_chain.py --tag <tag>`
- [ ] Record this interaction start in maintenance log:
  - `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`

---

## B. End-of-Interaction Checklist

Complete these before sending final response:

- [ ] Check whether this interaction produced reusable knowledge.
- [ ] If yes, update one or more docs under:
  - `docs/knowledge_base/`
  - `docs/pdk_tech/`
  - `docs/cts_algorithms/`
  - `docs/flow_reliability/`
- [ ] Update hypothesis-validation-conclusion record:
  - `docs/knowledge_base/90_HYPOTHESIS_VALIDATION_LOG.md`
- [ ] Check whether scripts/tools changed.
  - if changed, rebuild registry:
    - `python3 scripts/common/tool_catalog.py build`
- [ ] If route-level results are used, attach execution-contract artifact (`execution_contract.md`).
- [ ] If continuing optimization, ingest manifest to memory DB and produce proposal artifact.
- [ ] If this is a full research-chain task, run chain guard and link summary artifact:
  - `python3 scripts/common/research_chain_guard.py --chain-dir <chain_dir> --out-prefix <prefix>`
- [ ] If new script added, ensure it appears in:
  - `docs/tool_registry/tool_catalog.tsv`
  - `docs/tool_registry/tool_catalog.md`
- [ ] Record this interaction end in maintenance log:
  - what was updated,
  - why,
  - what remains.

---

## C. Minimum Reporting in Reply

Every final reply should include:

1. `KB used`: which knowledge docs were consulted.
2. `Web evidence`: which external/primary sources were consulted (or why not required).
3. `Tool search`: query keywords + selected script(s).
4. `KB/Tool updates`: what was updated this turn.
5. `Open items`: what still needs updates.

This keeps behavior auditable and prevents duplicate tooling.
