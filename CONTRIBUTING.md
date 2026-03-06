# Contributing to EDAgent

Thanks for testing and improving EDAgent.

## Before You Start
- This project is research-oriented and evolves quickly.
- Prefer small, focused changes with clear rationale.
- Do not submit secrets, proprietary datasets, or restricted PDK files.

## How to Report Issues
Please include:
1. Environment summary (`OS`, Python version, shell platform).
2. Reproduction steps (exact commands/prompts).
3. Expected behavior vs actual behavior.
4. Relevant artifacts/logs (paths under `slurm_logs/00_meta/` when possible).
5. Scope tag: `infra`, `skill`, `knowledge`, `flow`, or `docs`.

## Pull Request Guidelines
1. Keep each PR scoped to one purpose.
2. Update docs when behavior changes.
3. Preserve backward compatibility unless clearly justified.
4. Add rollback notes for infrastructure/policy changes.
5. Avoid broad refactors unless requested.

## Recommended Validation (for infra changes)
Run these checks before opening PR:
```bash
python3 scripts/common/tool_catalog.py query infra skill
python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_pr
python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_pr
python3 scripts/common/unified_kb_query.py build
```

## Review Criteria
PRs are reviewed for:
- clarity of intent,
- reproducibility,
- minimal risk,
- documentation completeness.

## Communication
For substantial changes, open an issue first with:
- problem statement,
- proposed approach,
- expected impact,
- rollback trigger.
