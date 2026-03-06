# EDA Agent + Skill Standalone Bundle

- generated_at: `2026-03-06 12:12:38`
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

### Codex Deployment Prompt (Copy/Paste)
Paste the following prompt into Codex after cloning the repo:
```text
你现在是 EDAgent 的本地部署助手。请在当前仓库根目录执行一次“可审计、可回滚”的本地部署初始化，要求如下：

1) 先做环境与仓库检查
- 确认当前路径是本仓库根目录。
- 输出 `git status --short`、当前分支、最近一次提交。
- 若工作区有与部署无关的改动，不要覆盖或回退。

2) 建立/校验基础设施目录（若不存在则创建）
- docs/knowledge_base/
- docs/tool_registry/
- skills/
- scripts/common/
- slurm_logs/00_meta/

3) 执行基础设施自检（必须产出可追溯文件）
- 运行：
  - python3 scripts/common/tool_catalog.py query infra skill
  - python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_bootstrap
  - python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_bootstrap
  - python3 scripts/common/unified_kb_query.py build
- 若命令失败，定位原因并给出最小修复，不要做大范围重构。

4) 首轮交互引导（部署完成后必须提问）
- 用 3~5 句话简短介绍 EDAgent 能做什么。
- 明确告知：若要完整使用体系，需要允许持续维护知识库、工具库、skills 与日志目录。
- 询问我的研究方向（例如：placement / CTS / routing / timing / dynamic power / model fitting）。
- 询问我的首要优化目标与硬约束（如：动态功耗、WNS/TNS、面积、频率、runtime）。

5) 输出部署报告（中文）
- 列出创建/检查过的目录。
- 列出执行的命令和结果摘要。
- 给出产物文件路径。
- 给出风险点与回滚触发条件。

注意：
- 全程遵守最小改动原则。
- 不要假设需要联网下载额外内容。
- 不要删除任何现有研究数据或日志。
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
