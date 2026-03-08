#!/usr/bin/env python3
"""Bridge autoIdea outputs into this repo's paper/knowledge/idea infrastructure."""

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def slug(s: str) -> str:
    x = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return x or "unknown"


def parse_recommended_top30(path: Path) -> List[Tuple[str, float]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    out: List[Tuple[str, float]] = []
    for it in data:
        if isinstance(it, list) and len(it) >= 2:
            title = str(it[0]).strip()
            try:
                score = float(it[1])
            except Exception:
                score = 0.0
            if title:
                out.append((title, score))
    return out


def dedup_titles(items: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    best: Dict[str, float] = {}
    best_title: Dict[str, str] = {}
    for title, score in items:
        k = slug(title)
        if k not in best or score > best[k]:
            best[k] = score
            best_title[k] = title
    out = [(best_title[k], best[k]) for k in best]
    out.sort(key=lambda x: x[1], reverse=True)
    return out


def build_queue(autoidea_root: Path, out_tsv: Path, top_n: int) -> int:
    rec_path = autoidea_root / "citation_graph_output" / "recommended_top30.json"
    items = dedup_titles(parse_recommended_top30(rec_path))
    items = items[:top_n]

    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "rank",
        "priority",
        "source",
        "title",
        "score",
        "first_author_hint",
        "why_selected",
        "status",
    ]
    with out_tsv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=fields)
        w.writeheader()
        for i, (title, score) in enumerate(items, start=1):
            w.writerow(
                {
                    "rank": i,
                    "priority": "high" if i <= 10 else "medium",
                    "source": "autoIdea.recommended_top30",
                    "title": title,
                    "score": f"{score:.6f}",
                    "first_author_hint": "",
                    "why_selected": "citation/semantic expansion from local BSPDN corpus",
                    "status": "todo",
                }
            )
    return len(items)


def merge_with_feedback(feedback_queue: Path, autoidea_queue: Path, out_tsv: Path) -> int:
    rows = []
    if feedback_queue.exists():
        with feedback_queue.open("r", encoding="utf-8", errors="ignore") as f:
            rows.extend(list(csv.DictReader(f, delimiter="\t")))

    auto_rows = []
    if autoidea_queue.exists():
        with autoidea_queue.open("r", encoding="utf-8", errors="ignore") as f:
            auto_rows = list(csv.DictReader(f, delimiter="\t"))

    for r in auto_rows:
        rows.append(
            {
                "queue_id": f"AUTO_{r.get('rank','')}",
                "priority": r.get("priority", "medium"),
                "type": "autoidea_recommendation",
                "target_subproblem": "",
                "target_method": "",
                "reason": r.get("why_selected", ""),
                "query": r.get("title", ""),
                "status": r.get("status", "todo"),
            }
        )

    # Dedup by normalized query
    out_rows = []
    seen = set()
    for r in rows:
        q = re.sub(r"\s+", " ", (r.get("query", "").lower())).strip()
        if not q:
            continue
        if q in seen:
            continue
        seen.add(q)
        out_rows.append(r)

    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    fields = ["queue_id", "priority", "type", "target_subproblem", "target_method", "reason", "query", "status"]
    with out_tsv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(out_rows, start=1):
            if not r.get("queue_id"):
                r["queue_id"] = f"MERGED{i:03d}"
            w.writerow({k: r.get(k, "") for k in fields})

    return len(out_rows)


def write_fusion_report(autoidea_root: Path, out_md: Path, auto_count: int, merged_count: int) -> None:
    final_idea = read_text(autoidea_root / "outputs" / "final_idea.txt")
    experiment = read_text(autoidea_root / "outputs" / "experiment.txt")
    hist_pf = read_text(autoidea_root / "citation_graph_output" / "historical_problem_formulation.txt")

    lines: List[str] = []
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append("# AutoIdea Fusion Report")
    lines.append("")
    lines.append(f"- timestamp: `{ts}`")
    lines.append(f"- autoidea_root: `{autoidea_root}`")
    lines.append(f"- imported_recommendation_count: `{auto_count}`")
    lines.append(f"- merged_queue_count: `{merged_count}`")
    lines.append("")

    lines.append("## Imported Artifacts")
    lines.append("- paper recommendation queue: `docs/papers/queues/autoidea_recommended_top30_bridge.tsv`")
    lines.append("- merged retrieval queue: `docs/papers/queues/literature_feedback_merged_with_autoidea.tsv`")
    lines.append("- this report: `docs/knowledge_base/99_AUTOIDEA_FUSION_REPORT_20260306.md`")
    lines.append("")

    lines.append("## Strengths Borrowed from autoIdea")
    lines.append("1. Citation/semantic expansion around local corpus (`recommended_top30`).")
    lines.append("2. Structured problem-formulation abstraction from historical literature.")
    lines.append("3. Debate-style idea and experiment draft generation.")
    lines.append("")

    lines.append("## Fusion Mapping into Current Skill Stack")
    lines.append("- `eda-paper-fetch`: prioritize `autoidea_recommended_top30_bridge.tsv` for targeted download.")
    lines.append("- `paper_kb_index` + landscape pipeline: absorb downloaded/summarized papers into 95/96/97/98 artifacts.")
    lines.append("- `eda-idea-debate-lab` / `eda-hypothesis-experiment-designer`: use imported idea+experiment draft as initial candidate, then apply theory veto and non-regression gates.")
    lines.append("")

    if final_idea:
        lines.append("## Imported Idea Draft (from autoIdea)")
        lines.append("```text")
        lines.extend(final_idea.splitlines()[:120])
        lines.append("```")
        lines.append("")

    if experiment:
        lines.append("## Imported Experiment Draft (from autoIdea)")
        lines.append("```text")
        lines.extend(experiment.splitlines()[:180])
        lines.append("```")
        lines.append("")

    if hist_pf:
        lines.append("## Imported Historical Formulation Notes")
        lines.append("```text")
        lines.extend(hist_pf.splitlines()[:120])
        lines.append("```")
        lines.append("")

    lines.append("## Next Actions")
    lines.append("1. Run `eda-paper-fetch` over top high-priority merged queue rows.")
    lines.append("2. Download + summarize PDFs, then run `paper_kb_index.py build`.")
    lines.append("3. Re-run `autoidea_bridge.py` and compare `98_LITERATURE_FEEDBACK_LOOP.md` gap counts.")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Bridge autoIdea outputs into current skill/knowledge flow")
    ap.add_argument("--autoidea-root", default="external_tools/autoIdea")
    ap.add_argument("--top-n", type=int, default=30)
    args = ap.parse_args()

    autoidea_root = Path(args.autoidea_root)
    auto_queue = ROOT / "docs" / "papers" / "queues" / "autoidea_recommended_top30_bridge.tsv"
    feedback_queue = ROOT / "docs" / "papers" / "queues" / "literature_feedback_queue.tsv"
    merged_queue = ROOT / "docs" / "papers" / "queues" / "literature_feedback_merged_with_autoidea.tsv"
    report = ROOT / "docs" / "knowledge_base" / "99_AUTOIDEA_FUSION_REPORT_20260306.md"

    count = build_queue(autoidea_root, auto_queue, args.top_n)
    merged_count = merge_with_feedback(feedback_queue, auto_queue, merged_queue)
    write_fusion_report(autoidea_root, report, count, merged_count)

    print(f"wrote: {auto_queue}")
    print(f"wrote: {merged_queue}")
    print(f"wrote: {report}")
    print(f"autoidea_rows={count}")
    print(f"merged_rows={merged_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
