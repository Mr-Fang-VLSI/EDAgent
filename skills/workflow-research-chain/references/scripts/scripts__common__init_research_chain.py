#!/usr/bin/env python3
"""Initialize a full EDA research-chain workspace with stage folders and starter artifacts."""

import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE = ROOT / "slurm_logs" / "05_research_chain"


STAGES: List[Tuple[str, str]] = [
    ("00_bootstrap", "task_brief.md"),
    ("01_knowledge", "knowledge_gap_map.md"),
    ("02_literature", "paper_download_queue.tsv"),
    ("02_literature", "local_paper_summary_index.md"),
    ("03_idea_debate", "idea_brainstorm.md"),
    ("03_idea_debate", "pro_con_debate.md"),
    ("04_hypothesis_design", "hypothesis_experiment_matrix.tsv"),
    ("05_implementation", "implementation_plan.md"),
    ("06_versioning", "version_plan.md"),
    ("07_validation", "validation_summary.md"),
    ("08_retro", "research_retro.md"),
]


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Initialize an EDA research-chain workspace")
    ap.add_argument("--tag", default=None, help="chain tag; defaults to timestamp")
    ap.add_argument("--base-dir", default=str(DEFAULT_BASE), help="base directory for chain workspaces")
    return ap.parse_args()


def write_if_missing(path: Path, text: str) -> None:
    if path.exists():
        return
    path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    tag = args.tag or datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = Path(args.base_dir)
    chain_dir = base_dir / tag
    chain_dir.mkdir(parents=True, exist_ok=True)

    template_task = ROOT / "docs" / "knowledge_base" / "templates" / "research_chain_task_brief_template.md"
    template_idea = ROOT / "docs" / "knowledge_base" / "templates" / "idea_debate_note_template.md"
    template_hypo = ROOT / "docs" / "knowledge_base" / "templates" / "hypothesis_experiment_matrix_template.tsv"

    for folder, filename in STAGES:
        d = chain_dir / folder
        d.mkdir(parents=True, exist_ok=True)
        p = d / filename
        if filename == "task_brief.md" and template_task.is_file():
            write_if_missing(p, template_task.read_text(encoding="utf-8", errors="ignore"))
        elif filename in {"idea_brainstorm.md", "pro_con_debate.md"} and template_idea.is_file():
            write_if_missing(p, template_idea.read_text(encoding="utf-8", errors="ignore"))
        elif filename == "hypothesis_experiment_matrix.tsv" and template_hypo.is_file():
            write_if_missing(p, template_hypo.read_text(encoding="utf-8", errors="ignore"))
        elif filename.endswith(".tsv"):
            write_if_missing(p, "")
        else:
            write_if_missing(p, f"# {filename}\n\n")

    manifest = chain_dir / "chain_manifest.tsv"
    if not manifest.exists():
        lines = ["stage\trequired_file\tstatus\tnote"]
        for folder, filename in STAGES:
            lines.append(f"{folder}\t{folder}/{filename}\tpending\t")
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    readme = chain_dir / "README.md"
    if not readme.exists():
        readme.write_text(
            "\n".join(
                [
                    "# Research Chain Workspace",
                    "",
                    f"- tag: `{tag}`",
                    f"- created_at: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
                    "- use `chain_manifest.tsv` to track stage completion.",
                    "- validate completeness with:",
                    f"  - `python3 scripts/common/research_chain_guard.py --chain-dir {chain_dir}`",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    print(f"chain_dir={chain_dir}")
    print(f"manifest={manifest}")
    print(f"readme={readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
