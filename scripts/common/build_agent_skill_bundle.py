#!/usr/bin/env python3
"""Build standalone bundle for agent+skill system.

The bundle is self-contained for governance docs and skill-local script mirrors.
"""

from __future__ import annotations

import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parents[2]


def safe_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree_filtered(src: Path, dst: Path, ignore_names: Set[str] | None = None) -> None:
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
    git_backup: Path | None = None
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
        'knowledge_gate.sh',
        'paper_kb_index.py',
        'paper_landscape_sync.py',
        'paper_landscape_feedback.py',
        'unified_kb_query.py',
        'autoidea_bridge.py',
        'build_agent_skill_bundle.py',
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
                '- `python3` (3.10+ recommended)',
                '- `git`',
                '',
                '### Two-Step Onboarding (Recommended)',
                '```bash',
                'git clone https://github.com/Mr-Fang-VLSI/EDAgent.git',
                'cd EDAgent',
                'python3 run_demo.py',
                '```',
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
                'Manual checks (optional):',
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

    (out_dir / 'run_demo.py').write_text(
        "\n".join(
            [
                '#!/usr/bin/env python3',
                '"""One-command local bootstrap demo for EDAgent."""',
                '',
                'from __future__ import annotations',
                '',
                'import subprocess',
                'import sys',
                'from pathlib import Path',
                'from typing import List, Tuple',
                '',
                '',
                'ROOT = Path(__file__).resolve().parent',
                '',
                '',
                'def run_step(name: str, cmd: List[str]) -> Tuple[bool, str]:',
                '    try:',
                '        out = subprocess.run(',
                '            cmd,',
                '            cwd=ROOT,',
                '            check=True,',
                '            text=True,',
                '            capture_output=True,',
                '        )',
                '        return True, out.stdout.strip()',
                '    except subprocess.CalledProcessError as e:',
                '        msg = (e.stdout or "") + ("\\n" + e.stderr if e.stderr else "")',
                '        return False, msg.strip()',
                '',
                '',
                'def main() -> int:',
                '    required_dirs = [',
                '        ROOT / "docs" / "knowledge_base",',
                '        ROOT / "docs" / "tool_registry",',
                '        ROOT / "skills",',
                '        ROOT / "scripts" / "common",',
                '        ROOT / "slurm_logs" / "00_meta",',
                '    ]',
                '    for d in required_dirs:',
                '        d.mkdir(parents=True, exist_ok=True)',
                '',
                '    steps = [',
                '        ("tool catalog query", ["python3", "scripts/common/tool_catalog.py", "query", "infra", "skill"]),',
                '        (',
                '            "infra stack guard",',
                '            [',
                '                "python3",',
                '                "scripts/common/infra_stack_guard.py",',
                '                "--out-prefix",',
                '                "slurm_logs/00_meta/infra_stack_guard_bootstrap",',
                '            ],',
                '        ),',
                '        (',
                '            "skill system audit",',
                '            [',
                '                "python3",',
                '                "scripts/common/skill_system_audit.py",',
                '                "--out-prefix",',
                '                "slurm_logs/00_meta/skill_system_audit_bootstrap",',
                '            ],',
                '        ),',
                '        ("kb index build", ["python3", "scripts/common/unified_kb_query.py", "build"]),',
                '    ]',
                '',
                '    print("EDAgent demo bootstrap start")',
                '    failed_steps = []',
                '    for name, cmd in steps:',
                '        ok, output = run_step(name, cmd)',
                '        status = "OK" if ok else "FAIL"',
                '        print(f"[{status}] {name}: {\' \'.join(cmd)}")',
                '        if output:',
                '            lines = output.splitlines()',
                '            preview = "\\n".join(lines[:8])',
                '            print(preview)',
                '            if len(lines) > 8:',
                '                print("... (truncated)")',
                '        if not ok:',
                '            failed_steps.append(name)',
                '',
                '    print()',
                '    if failed_steps:',
                '        print("Bootstrap finished with warnings.")',
                '        print("Failed checks: " + ", ".join(failed_steps))',
                '        print("You can still start with EDAgent; fix warnings for full governance mode.")',
                '    else:',
                '        print("Bootstrap complete.")',
                '    print("Next, ask EDAgent your research direction and target constraints.")',
                '    print("Example: \'My focus is placement for dynamic-power reduction with area/timing guardrails.\'")',
                '    return 0',
                '',
                '',
                'if __name__ == "__main__":',
                '    sys.exit(main())',
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
