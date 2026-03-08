#!/usr/bin/env python3
"""Build standalone bundle for agent+skill system.

The bundle is self-contained for governance docs and skill-local script mirrors.
"""

import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

ROOT = Path(__file__).resolve().parents[2]


def safe_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree_filtered(src: Path, dst: Path, ignore_names: Optional[Set[str]] = None) -> None:
    ignore_names = ignore_names or set()
    if dst.exists():
        shutil.rmtree(dst)

    def _ignore(_dir: str, names: List[str]) -> Set[str]:
        out = set()
        for n in names:
            if n in ignore_names:
                out.add(n)
            if n.endswith('.zip'):
                out.add(n)
            if n == '__pycache__':
                out.add(n)
        return out

    shutil.copytree(src, dst, ignore=_ignore)


def load_tool_map(catalog_tsv: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    with catalog_tsv.open('r', encoding='utf-8', errors='ignore') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            tid = (row.get('tool_id') or '').strip()
            path = (row.get('path') or '').strip()
            if tid and path:
                out[tid] = path
    return out


def load_manifest(path: Path) -> List[Dict[str, str]]:
    with path.open('r', encoding='utf-8', errors='ignore') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_manifest(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        w.writeheader()
        w.writerows(rows)


def normalize_filename(rel_path: str) -> str:
    return rel_path.replace('/', '__')


def build_bundle(out_dir: Path) -> None:
    git_backup = None  # type: Optional[Path]
    if out_dir.exists():
        git_dir = out_dir / '.git'
        if git_dir.exists():
            git_backup = out_dir.parent / f'.{out_dir.name}.git.backup'
            if git_backup.exists():
                shutil.rmtree(git_backup)
            shutil.move(str(git_dir), str(git_backup))
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if git_backup and git_backup.exists():
        shutil.move(str(git_backup), str(out_dir / '.git'))

    # Core files/dirs
    safe_copy(ROOT / 'AGENTS.md', out_dir / 'AGENTS.md')
    copy_tree_filtered(ROOT / 'skills', out_dir / 'skills')

    kb_keep = {
        'README.md',
        '00_START_HERE.md',
        '10_TASK_EXECUTION_PROTOCOL.md',
        '11_INTERACTION_CHECKLIST.md',
        '90_HYPOTHESIS_VALIDATION_LOG.md',
        '92_INFRASTRUCTURE_STEWARDSHIP_20260306.md',
        '93_EDA_RESEARCH_FULL_CHAIN_20260306.md',
        '95_PROBLEM_LANDSCAPE.md',
        '96_METHOD_LANDSCAPE.md',
        '97_GLOBAL_RESEARCH_LANDSCAPE.md',
        '98_LITERATURE_FEEDBACK_LOOP.md',
        '99_AUTOIDEA_FUSION_REPORT_20260306.md',
    }
    (out_dir / 'docs' / 'knowledge_base').mkdir(parents=True, exist_ok=True)
    for name in kb_keep:
        src = ROOT / 'docs' / 'knowledge_base' / name
        if src.exists():
            safe_copy(src, out_dir / 'docs' / 'knowledge_base' / name)

    tool_registry_keep = {'README.md', 'tool_catalog.tsv', 'tool_catalog.md', 'tool_metadata.tsv'}
    (out_dir / 'docs' / 'tool_registry').mkdir(parents=True, exist_ok=True)
    for name in tool_registry_keep:
        src = ROOT / 'docs' / 'tool_registry' / name
        if src.exists():
            safe_copy(src, out_dir / 'docs' / 'tool_registry' / name)

    # scripts/common for infra bootstrapping
    common_keep = {
        'tool_catalog.py',
        'skill_system_audit.py',
        'infra_stack_guard.py',
        'init_research_chain.py',
        'knowledge_gate.sh',
        'paper_kb_index.py',
        'paper_landscape_sync.py',
        'paper_landscape_feedback.py',
        'research_chain_guard.py',
        'unified_kb_query.py',
        'autoidea_bridge.py',
        'build_agent_skill_bundle.py',
        'conda_project_env_report.py',
    }
    (out_dir / 'scripts' / 'common').mkdir(parents=True, exist_ok=True)
    for name in common_keep:
        src = ROOT / 'scripts' / 'common' / name
        if src.exists():
            safe_copy(src, out_dir / 'scripts' / 'common' / name)

    # skill-local mirrors for dependent tools
    catalog = load_tool_map(ROOT / 'docs' / 'tool_registry' / 'tool_catalog.tsv')
    manifest_src = ROOT / 'skills' / '00_SKILL_SYSTEM_MANIFEST.tsv'
    rows = load_manifest(manifest_src)
    fields = list(rows[0].keys()) if rows else []
    if 'skill_local_tools' not in fields:
        fields.append('skill_local_tools')

    external_allow = {'git', 'python3', 'bash', 'node'}
    for r in rows:
        skill = r['skill']
        deps = [x.strip() for x in (r.get('depends_on_tools') or '').split(',') if x.strip()]
        local_refs: List[str] = []
        skill_script_dir = out_dir / 'skills' / skill / 'references' / 'scripts'
        for dep in deps:
            if dep in external_allow:
                continue
            rel = catalog.get(dep, '')
            if not rel:
                continue
            src = ROOT / rel
            if not src.exists() or not src.is_file():
                continue
            local_name = normalize_filename(rel)
            dst = skill_script_dir / local_name
            safe_copy(src, dst)
            local_refs.append(str(Path('skills') / skill / 'references' / 'scripts' / local_name))
        r['skill_local_tools'] = ','.join(local_refs)

    write_manifest(out_dir / 'skills' / '00_SKILL_SYSTEM_MANIFEST.tsv', rows, fields)

    # standalone readme
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    readme = out_dir / 'README.md'
    readme.write_text(
        "\n".join(
            [
                '# EDA Agent + Skill Standalone Bundle',
                '',
                f'- generated_at: `{ts}`',
                f'- source_repo: `{ROOT}`',
                '',
                '## What It Can Do',
                '- Govern end-to-end EDA research workflow from idea to validation and retrospective.',
                '- Manage literature flow: retrieval, local PDF parsing, evidence indexing, and landscape updates.',
                '- Run gated execution loops with theory-veto, experiment contracts, and maintenance audits.',
                '- Maintain a skill-based automation stack with tool catalog, knowledge base, and manifest governance.',
                '',
                '## Open-Source Scope',
                '- This repository is for research and experimentation.',
                '- No production SLA, no warranty, and no guarantee of correctness for all environments.',
                '- Please validate results independently before any high-stakes use.',
                '- See `CONTRIBUTING.md` for contribution workflow and `ROADMAP.md` for current priorities.',
                '',
                '## Installation',
                '### Prerequisites',
                '- Linux/macOS shell environment',
                '- `python3` (3.6+ for bootstrap; newer recommended for optional utilities)',
                '- `git`',
                '',
                '### Codex Deployment Prompt (Copy/Paste)',
                'Paste the following prompt into Codex after cloning the repo:',
                '```text',
                'You are EDAgent local deployment assistant. In the current repository root, perform one auditable and rollback-safe local deployment bootstrap with the following requirements:',
                '',
                '1) Environment and repository checks first',
                '- Confirm the current path is the repository root.',
                '- Report `git status --short`, current branch, and latest commit.',
                '- If there are unrelated working-tree changes, do not overwrite or revert them.',
                '',
                '2) Create/verify infrastructure directories (create if missing)',
                '- docs/knowledge_base/',
                '- docs/tool_registry/',
                '- skills/',
                '- scripts/common/',
                '- slurm_logs/00_meta/',
                '',
                '3) Run infrastructure self-checks (must produce traceable artifacts)',
                '- Run:',
                '  - python3 scripts/common/tool_catalog.py query infra skill',
                '  - python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_bootstrap',
                '  - python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_bootstrap',
                '  - python3 scripts/common/unified_kb_query.py build',
                '- If a command fails, locate the root cause and apply minimal fixes only (no broad refactor).',
                '',
                '4) First interaction onboarding (must ask after deployment)',
                '- Briefly introduce what EDAgent can do in 3-5 sentences.',
                '- Explicitly state that full usage requires permission to maintain KB/tool/skills/log infrastructure.',
                '- Ask for my current research direction (e.g., placement / CTS / routing / timing / dynamic power / model fitting).',
                '- Ask for my top optimization target and hard constraints (e.g., dynamic power, WNS/TNS, area, frequency, runtime).',
                '',
                '5) Output deployment report (English)',
                '- List created/verified directories.',
                '- List executed commands and summary results.',
                '- Provide artifact file paths.',
                '- Provide risk points and rollback triggers.',
                '',
                'Notes:',
                '- Follow the minimal-change principle throughout.',
                '- Do not assume internet access for extra downloads.',
                '- Do not delete any existing research data or logs.',
                '```',
                '',
                '### Quick Start',
                '```bash',
                'git clone https://github.com/Mr-Fang-VLSI/EDAgent.git',
                'cd EDAgent',
                'python3 scripts/common/tool_catalog.py query infra skill',
                'python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_bootstrap',
                'python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_bootstrap',
                '```',
                '',
                '## System Composition',
                '- `AGENTS.md`: top-level policy and cross-skill governance boundary.',
                '- `skills/`: executable capability units (orchestration, research chain, domain methods, infra maintenance).',
                '- `docs/knowledge_base/`: protocol, landscape, and governance knowledge.',
                '- `docs/tool_registry/`: tool metadata/catalog for discoverability and lifecycle control.',
                '- `scripts/common/`: reusable infrastructure scripts.',
                '- `skills/<skill>/references/scripts/`: skill-local mirrored script dependencies for portability.',
                '',
                '## Layered Design',
                'The system is intentionally layered so policy, orchestration, reusable utilities, and domain logic do not collapse into one giant prompt.',
                '',
                '### Layer 0: Governance and contracts',
                '- `AGENTS.md` defines repo-wide rules: routing disclosure, workflow ownership, promotion locks, maintenance checks, and output contracts.',
                '- This layer answers: what must be disclosed, what is allowed to change, and what evidence is required before expensive execution.',
                '',
                '### Layer 1: Workflow and control-plane owners',
                '- `workflow-router` decides which workflow applies and which skill should own orchestration.',
                '- `workflow-scoped-execution` owns one bounded governed execution task.',
                '- `workflow-research-chain` owns multi-stage idea -> hypothesis -> implementation -> validation flows.',
                '- `control-*` skills such as `control-theory-veto`, `control-preflight-reflect`, and `control-postrun-retro` act as gates around execution rather than domain implementers.',
                '',
                '### Layer 2: Horizontal utility skills',
                '- Utilities do not own final research claims; they provide reusable support across workflows.',
                '- Examples: `eda-infra-maintainer`, `eda-context-accessor`, `eda-knowledge-gate-maintainer`, `eda-experiment-phenomenology-analyst`, `eda-script-pattern-curator`, and `git-version-control`.',
                '- These skills exist so shared logic like KB retrieval, artifact hygiene, versioning, and experiment-evidence lifting is implemented once.',
                '',
                '### Layer 3: Domain and validation specialists',
                '- Domain skills own bounded technical expertise such as backside routing policy, BSPDN physical audit, cost modeling, or delay-model gates.',
                '- Examples: `gt3-backside-route-policy`, `bscost-theory-opt`, `delay-model-gate-evaluator`, `bspdn-physical-contract-auditor`, and `backside-routing-realization-specialist`.',
                '- These skills should answer domain questions directly without taking over repo-wide orchestration.',
                '',
                '### Layer 4: Knowledge and tools',
                '- `docs/knowledge_base/` stores durable knowledge, protocol, and paper-derived evidence.',
                '- `docs/tool_registry/` records stable tool identity, lifecycle, and ownership.',
                '- `scripts/common/` and skill-local mirrored scripts provide executable tooling.',
                '- The design rule is: skills connect to knowledge and tools, instead of duplicating them.',
                '',
                '## Design Rationale',
                '- Keep workflow-owner skills stable; add new domain behavior lower in the stack when possible.',
                '- Keep theory and practice coupled by feeding finished-run evidence into future gates and retrospectives.',
                '- Keep reusable utilities horizontal so multiple skills do not grow slightly different copies of the same logic.',
                '- Keep exportability high by mirroring skill-local script dependencies inside `skills/<skill>/references/scripts/`.',
                '',
                '## How Routing Usually Works',
                'A typical request is handled in this order:',
                '1. `workflow-router` classifies the task and selects one workflow owner.',
                '2. The workflow owner decides whether control/gate skills are needed.',
                '3. Utility skills provide shared retrieval, audit, hygiene, or versioning support.',
                '4. Domain skills perform the technical reasoning or implementation.',
                '5. Artifacts are written back to logs, KB, or version history.',
                '',
                'Example:',
                '- User asks: "run one bounded route-policy validation for GT3 and tell me if it is safe to continue."',
                '- Router outcome: `workflow-scoped-execution` as owner, with `control-theory-veto` and `gt3-backside-route-policy` in the active subset.',
                '- Result: execution stays bounded, while policy and veto logic remain reusable across later tasks.',
                '',
                '## Example Scenarios',
                '| Scenario | Recommended path | Why this path fits |',
                '|---|---|---|',
                '| I have a vague research direction and need literature -> idea -> hypothesis -> validation. | `workflow-router` -> `workflow-research-chain` -> `control-knowledge-explorer` / `eda-paper-fetch` / `eda-pdf-local-summary` / `eda-hypothesis-experiment-designer` / `eda-method-implementer` | This is a multi-stage chain, not a single execution step. |',
                '| I already know the exact bounded task, such as "run one governed route experiment" or "prepare one checkpointed execution stage". | `workflow-router` -> `workflow-scoped-execution` -> needed gate/domain skills | This keeps execution narrow and auditable instead of invoking the whole research chain. |',
                '| I want to improve BSPDN PPA toward explicit power/timing goals. | `workflow-router` -> `bspdn-goal-driver` -> `control-preflight-reflect` / `delay-model-gate-evaluator` / `gt3-backside-route-policy` / `git-version-control` | This is goal-driven iterative optimization with milestone gating. |',
                '| I suspect the local backside topology or layer/via assumptions are physically wrong. | `workflow-router` -> `bspdn-physical-contract-auditor` -> `control-knowledge-explorer` / `eda-paper-fetch` / `eda-pdf-local-summary` / `gt3-backside-route-policy` | This is a domain audit problem, not a generic execution wrapper problem. |',
                '| I finished a batch and want durable lessons instead of rereading raw monitor logs next week. | active workflow -> `eda-experiment-phenomenology-analyst` -> `control-postrun-retro` | This lifts `log -> result -> conclusion -> experience` for future reuse. |',
                '| I need to repair broken manifests, stale routing policy, or tool/skill drift. | `workflow-router` -> `eda-infra-maintainer` | This is maintenance of the system itself, not domain experimentation. |',
                '',
                '## Practical Entry Points',
                '- For first-time setup, run the bootstrap commands in `Quick Start` and then let the agent perform onboarding.',
                '- For research tasks, describe the goal in task language; the router is expected to choose the workflow and disclose it.',
                '- For maintenance tasks, say explicitly whether you want `use`, `maintain`, or `develop` behavior if you already know the intent.',
                '- For publishable evidence building, prefer workflows that leave guard/audit/version artifacts instead of ad hoc one-off commands.',
                '',
                '## First-Run Behavior (New Deployment)',
                '- Agent first introduces itself briefly.',
                '- Agent asks permission to bootstrap/maintain infrastructure folders:',
                '  - `docs/knowledge_base/`',
                '  - `docs/tool_registry/`',
                '  - `skills/`',
                '  - `scripts/common/`',
                '  - `slurm_logs/00_meta/`',
                '- Agent asks for current research direction and top optimization target/constraints before full execution.',
                '',
                '## Self-Development (Capability Growth)',
                '1. Add or refine a skill with clear boundary and interface version update.',
                '2. Register/refresh tool metadata in `docs/tool_registry/tool_metadata.tsv`.',
                '3. Rebuild/query catalog and update affected knowledge docs.',
                '4. Validate with infra guard + skill audit before promotion.',
                '',
                '## Self-Maintenance (Stability)',
                'Run periodic checks:',
                '```bash',
                'python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_periodic',
                'python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_periodic',
                'python3 scripts/common/tool_catalog.py query maintain audit',
                'python3 scripts/common/unified_kb_query.py build',
                '```',
                'Maintenance rule:',
                '- fix integrity drift first, then introduce new capability; every change needs rollback trigger notes.',
                '',
                '## Build/update bundle',
                '```bash',
                'python3 scripts/common/build_agent_skill_bundle.py --out-dir exports/eda_agent_skill_system',
                '```',
                '',
                '## Publish as GitHub repo',
                '```bash',
                'cd exports/eda_agent_skill_system',
                'git init',
                'git add .',
                'git commit -m "init standalone agent+skill system"',
                'git branch -M main',
                'git remote add origin <your-github-repo-url>',
                'git push -u origin main',
                '```',
            ]
        )
        + '\n',
        encoding='utf-8',
    )

    (out_dir / 'CONTRIBUTING.md').write_text(
        "\n".join(
            [
                '# Contributing to EDAgent',
                '',
                'Thanks for testing and improving EDAgent.',
                '',
                '## Before You Start',
                '- This project is research-oriented and evolves quickly.',
                '- Prefer small, focused changes with clear rationale.',
                '- Do not submit secrets, proprietary datasets, or restricted PDK files.',
                '',
                '## How to Report Issues',
                'Please include:',
                '1. Environment summary (`OS`, Python version, shell platform).',
                '2. Reproduction steps (exact commands/prompts).',
                '3. Expected behavior vs actual behavior.',
                '4. Relevant artifacts/logs (paths under `slurm_logs/00_meta/` when possible).',
                '5. Scope tag: `infra`, `skill`, `knowledge`, `flow`, or `docs`.',
                '',
                '## Pull Request Guidelines',
                '1. Keep each PR scoped to one purpose.',
                '2. Update docs when behavior changes.',
                '3. Preserve backward compatibility unless clearly justified.',
                '4. Add rollback notes for infrastructure/policy changes.',
                '5. Avoid broad refactors unless requested.',
                '',
                '## Recommended Validation (for infra changes)',
                'Run these checks before opening PR:',
                '```bash',
                'python3 scripts/common/tool_catalog.py query infra skill',
                'python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_pr',
                'python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_pr',
                'python3 scripts/common/unified_kb_query.py build',
                '```',
                '',
                '## Review Criteria',
                'PRs are reviewed for:',
                '- clarity of intent,',
                '- reproducibility,',
                '- minimal risk,',
                '- documentation completeness.',
                '',
                '## Communication',
                'For substantial changes, open an issue first with:',
                '- problem statement,',
                '- proposed approach,',
                '- expected impact,',
                '- rollback trigger.',
            ]
        )
        + '\n',
        encoding='utf-8',
    )

    (out_dir / 'ROADMAP.md').write_text(
        "\n".join(
            [
                '# EDAgent Roadmap',
                '',
                '## Current Priorities',
                '1. Stable onboarding and deployment across Codex/Claude-style environments.',
                '2. Stronger infrastructure governance (agent/skill boundaries, tool catalog integrity, auditability).',
                '3. Better paper-to-knowledge-to-experiment feedback loop.',
                '4. Faster iteration support for EDA experiment planning and retrospective loops.',
                '',
                '## Near-Term Milestones',
                '1. Improve first-run experience and reduce manual setup friction.',
                '2. Expand troubleshooting playbooks for common deployment/check failures.',
                '3. Harden retrieval quality for knowledge/tool lookup.',
                '4. Improve benchmark/case selection guidance for early-stage experiments.',
                '',
                '## Explicit Non-Goals (for now)',
                '1. Production-grade guarantees or SLA.',
                '2. Full automation of proprietary EDA toolchains requiring restricted assets.',
                '3. One-shot "final answer" optimization claims without staged evidence.',
                '',
                '## What We Need from Users',
                '1. Real-world bug reports with reproducible steps.',
                '2. Suggestions for missing skills/tooling boundaries.',
                '3. Evidence on where onboarding or workflow still feels heavy.',
                '',
                '## Update Policy',
                '- Roadmap is updated when priorities shift materially.',
                '- Keep changes concise and aligned with repository governance in `AGENTS.md`.',
            ]
        )
        + '\n',
        encoding='utf-8',
    )


def main() -> int:
    ap = argparse.ArgumentParser(description='Build standalone bundle for agent+skill system')
    ap.add_argument('--out-dir', default='exports/eda_agent_skill_system')
    args = ap.parse_args()

    out_dir = (ROOT / args.out_dir).resolve()
    build_bundle(out_dir)
    print(f'wrote_bundle: {out_dir}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
