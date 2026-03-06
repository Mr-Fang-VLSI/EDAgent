# EDA Agent + Skill Standalone Bundle

- generated_at: `2026-03-06 12:05:15`
- source_repo: `/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00`

## What It Can Do
- Govern end-to-end EDA research workflow from idea to validation and retrospective.
- Manage literature flow: retrieval, local PDF parsing, evidence indexing, and landscape updates.
- Run gated execution loops with theory-veto, experiment contracts, and maintenance audits.
- Maintain a skill-based automation stack with tool catalog, knowledge base, and manifest governance.

## Installation
### Prerequisites
- Linux/macOS shell environment
- `python3` (3.10+ recommended)
- `git`

### Quick Start
```bash
git clone https://github.com/Mr-Fang-VLSI/EDAgent.git
cd EDAgent
python3 scripts/common/tool_catalog.py query infra skill
python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_bootstrap
python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_bootstrap
```

## System Composition
- `agent.md`: top-level policy and cross-skill governance boundary.
- `skills/`: executable capability units (orchestration, research chain, domain methods, infra maintenance).
- `docs/knowledge_base/`: protocol, landscape, and governance knowledge.
- `docs/tool_registry/`: tool metadata/catalog for discoverability and lifecycle control.
- `scripts/common/`: reusable infrastructure scripts.
- `skills/<skill>/references/scripts/`: skill-local mirrored script dependencies for portability.

## Self-Development (Capability Growth)
1. Add or refine a skill with clear boundary and interface version update.
2. Register/refresh tool metadata in `docs/tool_registry/tool_metadata.tsv`.
3. Rebuild/query catalog and update affected knowledge docs.
4. Validate with infra guard + skill audit before promotion.

## Self-Maintenance (Stability)
Run periodic checks:
```bash
python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_periodic
python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_periodic
python3 scripts/common/tool_catalog.py query maintain audit
python3 scripts/common/unified_kb_query.py build
```
Maintenance rule:
- fix integrity drift first, then introduce new capability; every change needs rollback trigger notes.

## Build/update bundle
```bash
python3 scripts/common/build_agent_skill_bundle.py --out-dir exports/eda_agent_skill_system
```

## Publish as GitHub repo
```bash
cd exports/eda_agent_skill_system
git init
git add .
git commit -m "init standalone agent+skill system"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
