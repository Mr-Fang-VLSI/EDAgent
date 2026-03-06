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
    safe_copy(ROOT / 'agent.md', out_dir / 'agent.md')
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
                '## Installation',
                '### Prerequisites',
                '- Linux/macOS shell environment',
                '- `python3` (3.10+ recommended)',
                '- `git`',
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
                '- `agent.md`: top-level policy and cross-skill governance boundary.',
                '- `skills/`: executable capability units (orchestration, research chain, domain methods, infra maintenance).',
                '- `docs/knowledge_base/`: protocol, landscape, and governance knowledge.',
                '- `docs/tool_registry/`: tool metadata/catalog for discoverability and lifecycle control.',
                '- `scripts/common/`: reusable infrastructure scripts.',
                '- `skills/<skill>/references/scripts/`: skill-local mirrored script dependencies for portability.',
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
