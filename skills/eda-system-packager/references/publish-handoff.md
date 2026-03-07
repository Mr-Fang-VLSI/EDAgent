# Publish Handoff

Use this reference when the package must be turned into a repository-ready handoff.

## Typical Sequence

```bash
cd exports/eda_agent_skill_system
git init
git add .
git commit -m "init standalone agent+skill system"
git branch -M main
git remote add origin <repo_url>
git push -u origin main
```

## Handoff Rule

Record whether the package is intended for:
1. local archive only,
2. release mirror refresh,
3. external publication.
