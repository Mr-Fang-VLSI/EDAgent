---
name: eda-infra-maintainer
description: Maintain and evolve the EDA infrastructure stack (agent policy, knowledge base, tool registry, and skill system) with auditable guardrails and minimal-risk updates.
---

# EDA Infra Maintainer

## When to use

Use this skill when the user asks to:
1. improve/repair infrastructure (`knowledge_base`, `tool_registry`, `skills`, `agent` policy),
2. harden governance and reliability checks,
3. add new infrastructure capability for future research loops,
4. maintain full-chain research workflow infrastructure (`init_research_chain`, `research_chain_guard`, chain templates/skills).

## Scope boundary

This skill owns infrastructure governance and integrity.
It does not own domain experiment conclusions (timing/power/route/model physics).

## Workflow

1. Classify request mode:
- `use`: consume existing infra only.
- `maintain`: repair consistency/integrity.
- `develop`: add infra capability with boundary + rollback note.

2. Run baseline checks:

```bash
python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_<tag>
python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_<tag>
python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>
```

3. Apply minimal high-impact updates:
- prefer tightening contract/routing/checklist first,
- avoid broad rewrites unless explicitly requested.

4. Validate modified skills:

```bash
python3 /home/grads/d/donghao/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill_path>
```

5. Report:
- changed files,
- guard/audit artifact paths,
- residual risk and rollback trigger.

## Hard rules

1. Do not mix infrastructure governance with domain result claims.
2. Do not change comparison policy locks silently.
3. If critical guard checks fail, block promotion and fix first.

## Reference

Load when needed:
1. `references/maintenance-checklist.md`
