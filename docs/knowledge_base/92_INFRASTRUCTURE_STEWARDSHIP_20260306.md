# 92 Infrastructure Stewardship Contract (2026-03-06)

## Goal
Ensure the EDA agent can reliably use, maintain, and develop core infrastructure:
1. knowledge base (`docs/knowledge_base/*`),
2. tool registry and reusable scripts (`docs/tool_registry/*`, `scripts/common/*`),
3. skills system (`skills/*`, manifest, routing, audits),
4. repo-level agent governance (`agent.md`).
5. research-chain workflow infrastructure (`init_research_chain`, `research_chain_guard`, chain skills).

## Operating modes
1. Use mode:
- run user task using existing infrastructure; avoid governance changes.
2. Maintain mode:
- repair drift/inconsistency with minimal behavior change.
3. Develop mode:
- add capability (new skill/guard/policy) with explicit boundary and rollback trigger.

## Mandatory checks for maintain/develop
1. infrastructure guard:
```bash
python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_<tag>
```
2. skill-system audit:
```bash
python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_<tag>
```
3. tool reuse query:
```bash
python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>
```
4. for full-chain requests, initialize and guard chain workspace:
```bash
python3 scripts/common/init_research_chain.py --tag <tag>
python3 scripts/common/research_chain_guard.py --chain-dir <dir> --out-prefix <prefix>
```

If critical checks fail, block promotion/claim and fix baseline first.

## Skill ownership
1. global policy owner: `agent.md`
2. scoped execution orchestrator: `eda-loop`
3. infrastructure maintenance owner: `eda-infra-maintainer`
4. gate hygiene utility: `eda-knowledge-gate-maintainer`

## Output contract for infrastructure interactions
1. changed file list,
2. infra guard artifact path,
3. skill-system audit artifact path,
4. residual risk + rollback trigger.
