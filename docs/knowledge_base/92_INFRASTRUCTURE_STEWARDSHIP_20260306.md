# 92 Infrastructure Stewardship Contract (2026-03-06)

## Goal
Ensure the EDA agent can reliably use, maintain, and develop core infrastructure:
1. knowledge base (`docs/knowledge_base/*`),
2. tool registry and reusable scripts (`docs/tool_registry/*`, `scripts/common/*`),
3. skills system (`skills/*`, manifest, routing, audits),
4. repo-level agent governance (`AGENTS.md`).
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
1. global policy owner: `AGENTS.md`
2. scoped execution orchestrator: `eda-loop`
3. infrastructure maintenance owner: `eda-infra-maintainer`
4. gate hygiene utility: `eda-knowledge-gate-maintainer`
5. workflow-routing helper: `workflow-router` (helper only; final routing ownership stays with agent)

## Workflow-first governance rule
For maintain/develop interactions, agent must explicitly decide:
1. whether the current request is a `known workflow` or an `unknown temporary workflow`,
2. which workflow-local skill subset is allowed,
3. whether existing skills are sufficient,
4. whether a new skill is justified by boundary clarity and specialization.

Temporary workflows are required when no existing workflow is a clean fit.
New skills are justified when reusable specialist logic would otherwise bloat orchestration skills.

## Development line vs release mirror
The current repo is the development authority.

Default rule:
1. all new infrastructure changes land in the current repo first,
2. `exports/eda_agent_skill_system` is treated as a release mirror,
3. do not propagate changes from the current repo into the release mirror automatically.

Promotion into the exported/public version requires explicit user intent such as:
1. `sync to EDAgent`,
2. `promote to export`,
3. `prepare release`.

Without explicit promotion intent, keep changes local to the current repo.

## Principle capture rule
When the user states a durable principle, governance preference, or workflow rule, agent must persist it.

Default persistence behavior:
1. classify it as a principle candidate,
2. decide whether it belongs in protocol, infrastructure governance, a dedicated SOP, or a skill-local contract,
3. write it into repo documentation,
4. record it in the maintenance log.

Do not leave durable principles only in chat context.

## Architecture-upgrade validation rule
When infrastructure work changes routing, workflow ownership, skill boundaries, or reference topology policy:
1. write down the expected benefit,
2. define a later validation window,
3. define what evidence would show the new structure did not help,
4. review that decision after enough real usage instead of treating the refactor itself as proof.

## Output contract for infrastructure interactions
1. changed file list,
2. infra guard artifact path,
3. skill-system audit artifact path,
4. residual risk + rollback trigger,
5. architecture-change validation plan when the change is structural rather than a narrow bug fix.
