#!/usr/bin/env python3
"""Check whether a research chain workspace has required stage artifacts."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


REQUIRED: List[Tuple[str, str, str]] = [
    ("critical", "00_bootstrap", "task_brief.md"),
    ("critical", "01_knowledge", "knowledge_gap_map.md"),
    ("critical", "02_literature", "paper_download_queue.tsv"),
    ("critical", "02_literature", "local_paper_summary_index.md"),
    ("critical", "03_idea_debate", "idea_brainstorm.md"),
    ("critical", "03_idea_debate", "pro_con_debate.md"),
    ("critical", "04_hypothesis_design", "hypothesis_experiment_matrix.tsv"),
    ("critical", "05_implementation", "implementation_plan.md"),
    ("critical", "06_versioning", "version_plan.md"),
    ("critical", "07_validation", "validation_summary.md"),
    ("critical", "08_retro", "research_retro.md"),
]


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Validate research-chain artifact completeness")
    ap.add_argument("--chain-dir", required=True, help="research chain workspace directory")
    ap.add_argument("--out-prefix", default=None, help="output prefix for tsv/md artifacts")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    chain_dir = Path(args.chain_dir).resolve()
    if not chain_dir.is_dir():
        raise SystemExit(f"chain_dir_not_found: {chain_dir}")

    if args.out_prefix:
        out_prefix = Path(args.out_prefix)
    else:
        out_prefix = chain_dir / "research_chain_guard"
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    out_tsv = out_prefix.with_suffix(".detail.tsv")
    out_md = out_prefix.with_suffix(".summary.md")

    rows = []
    critical_fail = 0
    for level, folder, filename in REQUIRED:
        rel = f"{folder}/{filename}"
        p = chain_dir / folder / filename
        exists = p.is_file()
        status = "PASS" if exists else "FAIL"
        if level == "critical" and not exists:
            critical_fail += 1
        rows.append([level, rel, status, "exists" if exists else "missing"])

    with out_tsv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["level", "required_file", "status", "detail"])
        for r in rows:
            w.writerow(r)

    lines = []
    lines.append("# Research Chain Guard Summary")
    lines.append("")
    lines.append(f"- timestamp: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append(f"- chain_dir: `{chain_dir}`")
    lines.append(f"- overall_status: `{'PASS' if critical_fail == 0 else 'FAIL'}`")
    lines.append(f"- critical_fail_count: `{critical_fail}`")
    lines.append("")
    lines.append("| required_file | status |")
    lines.append("|---|---|")
    for _, rel, status, _ in rows:
        lines.append(f"| `{rel}` | {status} |")
    lines.append("")
    lines.append("## Artifacts")
    lines.append(f"- detail_tsv: `{out_tsv}`")
    lines.append(f"- summary_md: `{out_md}`")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote: {out_tsv}")
    print(f"wrote: {out_md}")
    print(f"overall_status={'PASS' if critical_fail == 0 else 'FAIL'}")
    return 0 if critical_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
