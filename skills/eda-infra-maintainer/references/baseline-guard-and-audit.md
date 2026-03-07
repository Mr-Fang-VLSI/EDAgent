# Baseline Guard And Audit

Use this reference when an infrastructure task needs concrete pre/post validation commands.

## Standard Baseline

Run before edits:

```bash
python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_<tag>
python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_<tag>
```

Run before creating a new helper or wrapper:

```bash
python3 scripts/common/tool_catalog.py query <kw1> <kw2>
```

Run after touching a skill:

```bash
python3 /home/grads/d/donghao/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill_path>
```

## Selection Rule

1. Always run both repo-level guard and skill-system audit for `maintain` and `develop` work.
2. Tool query is mandatory when the change may introduce or duplicate a script/helper.
3. Validate only the skills actually touched, then re-run the repo audit for the final state.
