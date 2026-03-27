# EDA Agent + Skill Standalone Bundle

- generated_at: `2026-03-07 23:36:11`
- source_repo: `/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00`

## What It Can Do
- Govern end-to-end EDA research workflow from idea to validation and retrospective.
- Manage literature flow: retrieval, local PDF parsing, evidence indexing, and landscape updates.
- Run gated execution loops with theory-veto, experiment contracts, and maintenance audits.
- Maintain a skill-based automation stack with tool catalog, knowledge base, and manifest governance.

## Open-Source Scope
- This repository is for research and experimentation.
- Licensed under the MIT License; see `LICENSE`.
- No production SLA, no warranty, and no guarantee of correctness for all environments.
- Please validate results independently before any high-stakes use.
- See `CONTRIBUTING.md` for contribution workflow and `ROADMAP.md` for current priorities.

## Installation
### Prerequisites
- Linux/macOS shell environment
- `python3` (3.6+ for bootstrap; newer recommended for optional utilities)
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
- `AGENTS.md`: top-level policy and cross-skill governance boundary.
- `skills/`: executable capability units (orchestration, research chain, domain methods, infra maintenance).
- `docs/knowledge_base/`: protocol, landscape, and governance knowledge.
- `docs/tool_registry/`: tool metadata/catalog for discoverability and lifecycle control.
- `scripts/common/`: reusable infrastructure scripts.
- `skills/<skill>/references/scripts/`: skill-local mirrored script dependencies for portability.

## Layered Design
The system is intentionally layered so policy, orchestration, reusable utilities, and domain logic do not collapse into one giant prompt.

### Layer 0: Governance and contracts
- `AGENTS.md` defines repo-wide rules: routing disclosure, workflow ownership, promotion locks, maintenance checks, and output contracts.
- This layer answers: what must be disclosed, what is allowed to change, and what evidence is required before expensive execution.

### Layer 1: Workflow and control-plane owners
- `workflow-router` decides which workflow applies and which skill should own orchestration.
- `workflow-scoped-execution` owns one bounded governed execution task.
- `workflow-research-chain` owns multi-stage idea -> hypothesis -> implementation -> validation flows.
- `control-*` skills such as `control-theory-veto`, `control-preflight-reflect`, and `control-postrun-retro` act as gates around execution rather than domain implementers.

### Layer 2: Horizontal utility skills
- Utilities do not own final research claims; they provide reusable support across workflows.
- Examples: `eda-infra-maintainer`, `eda-context-accessor`, `eda-knowledge-gate-maintainer`, `eda-experiment-phenomenology-analyst`, `eda-script-pattern-curator`, and `git-version-control`.
- These skills exist so shared logic like KB retrieval, artifact hygiene, versioning, and experiment-evidence lifting is implemented once.

### Layer 3: Domain and validation specialists
- Domain skills own bounded technical expertise such as backside routing policy, BSPDN physical audit, cost modeling, or delay-model gates.
- Examples: `gt3-backside-route-policy`, `bscost-theory-opt`, `delay-model-gate-evaluator`, `bspdn-physical-contract-auditor`, and `backside-routing-realization-specialist`.
- These skills should answer domain questions directly without taking over repo-wide orchestration.

### Layer 4: Knowledge and tools
- `docs/knowledge_base/` stores durable knowledge, protocol, and paper-derived evidence.
- `docs/tool_registry/` records stable tool identity, lifecycle, and ownership.
- `scripts/common/` and skill-local mirrored scripts provide executable tooling.
- The design rule is: skills connect to knowledge and tools, instead of duplicating them.

## Design Rationale
- Keep workflow-owner skills stable; add new domain behavior lower in the stack when possible.
- Keep theory and practice coupled by feeding finished-run evidence into future gates and retrospectives.
- Keep reusable utilities horizontal so multiple skills do not grow slightly different copies of the same logic.
- Keep exportability high by mirroring skill-local script dependencies inside `skills/<skill>/references/scripts/`.

## How Routing Usually Works
A typical request is handled in this order:
1. `workflow-router` classifies the task and selects one workflow owner.
2. The workflow owner decides whether control/gate skills are needed.
3. Utility skills provide shared retrieval, audit, hygiene, or versioning support.
4. Domain skills perform the technical reasoning or implementation.
5. Artifacts are written back to logs, KB, or version history.

Example:
- User asks: "run one bounded route-policy validation for GT3 and tell me if it is safe to continue."
- Router outcome: `workflow-scoped-execution` as owner, with `control-theory-veto` and `gt3-backside-route-policy` in the active subset.
- Result: execution stays bounded, while policy and veto logic remain reusable across later tasks.

## Example Scenarios
| Scenario | Recommended path | Why this path fits |
|---|---|---|
| I have a vague research direction and need literature -> idea -> hypothesis -> validation. | `workflow-router` -> `workflow-research-chain` -> `control-knowledge-explorer` / `eda-paper-fetch` / `eda-pdf-local-summary` / `eda-hypothesis-experiment-designer` / `eda-method-implementer` | This is a multi-stage chain, not a single execution step. |
| I already know the exact bounded task, such as "run one governed route experiment" or "prepare one checkpointed execution stage". | `workflow-router` -> `workflow-scoped-execution` -> needed gate/domain skills | This keeps execution narrow and auditable instead of invoking the whole research chain. |
| I want to improve BSPDN PPA toward explicit power/timing goals. | `workflow-router` -> `bspdn-goal-driver` -> `control-preflight-reflect` / `delay-model-gate-evaluator` / `gt3-backside-route-policy` / `git-version-control` | This is goal-driven iterative optimization with milestone gating. |
| I suspect the local backside topology or layer/via assumptions are physically wrong. | `workflow-router` -> `bspdn-physical-contract-auditor` -> `control-knowledge-explorer` / `eda-paper-fetch` / `eda-pdf-local-summary` / `gt3-backside-route-policy` | This is a domain audit problem, not a generic execution wrapper problem. |
| I finished a batch and want durable lessons instead of rereading raw monitor logs next week. | active workflow -> `eda-experiment-phenomenology-analyst` -> `control-postrun-retro` | This lifts `log -> result -> conclusion -> experience` for future reuse. |
| I need to repair broken manifests, stale routing policy, or tool/skill drift. | `workflow-router` -> `eda-infra-maintainer` | This is maintenance of the system itself, not domain experimentation. |

## Practical Entry Points
- For first-time setup, run the bootstrap commands in `Quick Start` and then let the agent perform onboarding.
- For research tasks, describe the goal in task language; the router is expected to choose the workflow and disclose it.
- For maintenance tasks, say explicitly whether you want `use`, `maintain`, or `develop` behavior if you already know the intent.
- For publishable evidence building, prefer workflows that leave guard/audit/version artifacts instead of ad hoc one-off commands.

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
