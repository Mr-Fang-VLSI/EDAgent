---
name: eda-system-packager
description: Package the agent+skill infrastructure into a standalone, portable repository-ready bundle with skill-local tool mirrors.
---

# EDA System Packager

## When to use
Use this skill when you need to:
1. export current `AGENTS.md + skills + core KB/tool docs` as a standalone package,
2. mirror dependent scripts into each skill's `references/scripts` for portability,
3. prepare a repository-ready folder for separate GitHub publication.

## Run
```bash
python3 scripts/common/build_agent_skill_bundle.py --out-dir exports/eda_agent_skill_system
```

## Output
- `exports/eda_agent_skill_system/`
  - standalone `AGENTS.md`
  - `skills/` with `skill_local_tools` mapping and mirrored scripts
  - core `docs/knowledge_base` and `docs/tool_registry`
  - selected `scripts/common`

## Publish
```bash
cd exports/eda_agent_skill_system
git init
git add .
git commit -m "init standalone agent+skill system"
git branch -M main
git remote add origin <repo_url>
git push -u origin main
```
