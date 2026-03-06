# EDA Agent + Skill Standalone Bundle

- generated_at: `2026-03-06 12:20:57`
- source_repo: `/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00`

## What It Can Do
- Govern end-to-end EDA research workflow from idea to validation and retrospective.
- Manage literature flow: retrieval, local PDF parsing, evidence indexing, and landscape updates.
- Run gated execution loops with theory-veto, experiment contracts, and maintenance audits.
- Maintain a skill-based automation stack with tool catalog, knowledge base, and manifest governance.

## Open-Source Scope
- This repository is for research and experimentation.
- No production SLA, no warranty, and no guarantee of correctness for all environments.
- Please validate results independently before any high-stakes use.
- See `CONTRIBUTING.md` for contribution workflow and `ROADMAP.md` for current priorities.

## Installation
### Prerequisites
- Linux/macOS shell environment
- `python3` (3.10+ recommended)
- `git`

### Codex Deployment Prompt (Copy/Paste)
Paste the following prompt into Codex after cloning the repo:
```text
You are EDAgent local deployment assistant. In the current repository root, perform one auditable and rollback-safe local deployment bootstrap with the following requirements:

1) Environment and repository checks first
- Confirm the current path is the repository root.
- Report `git status --short`, current branch, and latest commit.
- If there are unrelated working-tree changes, do not overwrite or revert them.

2) Create/verify infrastructure directories (create if missing)
- docs/knowledge_base/
- docs/tool_registry/
- skills/
- scripts/common/
- slurm_logs/00_meta/

3) Run infrastructure self-checks (must produce traceable artifacts)
- Run:
  - python3 scripts/common/tool_catalog.py query infra skill
  - python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_bootstrap
  - python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_bootstrap
  - python3 scripts/common/unified_kb_query.py build
- If a command fails, locate the root cause and apply minimal fixes only (no broad refactor).

4) First interaction onboarding (must ask after deployment)
- Briefly introduce what EDAgent can do in 3-5 sentences.
- Explicitly state that full usage requires permission to maintain KB/tool/skills/log infrastructure.
- Ask for my current research direction (e.g., placement / CTS / routing / timing / dynamic power / model fitting).
- Ask for my top optimization target and hard constraints (e.g., dynamic power, WNS/TNS, area, frequency, runtime).

5) Output deployment report (English)
- List created/verified directories.
- List executed commands and summary results.
- Provide artifact file paths.
- Provide risk points and rollback triggers.

Notes:
- Follow the minimal-change principle throughout.
- Do not assume internet access for extra downloads.
- Do not delete any existing research data or logs.
```

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

## First-Run Behavior (New Deployment)
- Agent first introduces itself briefly.
- Agent asks permission to bootstrap/maintain infrastructure folders:
  - `docs/knowledge_base/`
  - `docs/tool_registry/`
  - `skills/`
  - `scripts/common/`
  - `slurm_logs/00_meta/`
- Agent asks for current research direction and top optimization target/constraints before full execution.

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
