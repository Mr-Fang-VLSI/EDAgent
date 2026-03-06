# Infrastructure Maintenance Checklist

## Pre-change
1. Confirm mode: `use` / `maintain` / `develop`.
2. Run:
- `python3 scripts/common/infra_stack_guard.py --out-prefix <prefix>`
- `python3 scripts/common/skill_system_audit.py --out-prefix <prefix>`
3. Query existing tools before creating new scripts:
- `python3 scripts/common/tool_catalog.py query <kw1> <kw2>`

## Change
1. Keep edits minimal and scoped to the confirmed gap.
2. Preserve agent/skill boundary in `AGENTS.md`.
3. Update manifest/routing if a new skill is introduced.

## Post-change
1. Validate changed skills with `quick_validate.py`.
2. Re-run infra guard and skill-system audit.
3. Report:
- changed files,
- artifact paths,
- residual risk + rollback trigger.
