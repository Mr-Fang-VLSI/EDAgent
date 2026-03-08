#!/usr/bin/env python3
"""Generate targeted literature feedback from global landscape coverage.

Outputs:
- docs/knowledge_base/98_LITERATURE_FEEDBACK_LOOP.md
- docs/papers/queues/literature_feedback_queue.tsv
"""

import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple

ROOT = Path(__file__).resolve().parents[2]
GLOBAL_TSV = ROOT / "docs" / "knowledge_base" / "index" / "global_research_landscape.tsv"
OUT_MD = ROOT / "docs" / "knowledge_base" / "98_LITERATURE_FEEDBACK_LOOP.md"
OUT_QUEUE = ROOT / "docs" / "papers" / "queues" / "literature_feedback_queue.tsv"


class Topic(NamedTuple):
    key: str
    label: str
    keywords: Tuple[str, ...]


SUBPROBLEMS: Dict[str, Topic] = {
    "P1": Topic("P1", "Routing Capacity & Congestion", ("placement", "routing", "congestion", "capacity-aware")),
    "P2": Topic("P2", "Backside Resource Allocation", ("backside routing", "front-vs-back assignment", "resource allocation")),
    "P3": Topic("P3", "Timing Closure Sensitivity", ("timing-driven placement", "critical path", "clock-data")),
    "P4": Topic("P4", "Dynamic Power Reduction Under Constraints", ("dynamic power", "switching power", "non-regression timing area")),
    "P5": Topic("P5", "Via/TSV & Interconnect Constraints", ("nTSV", "via resistance", "interconnect parasitics")),
    "P6": Topic("P6", "Legality & Detailed Placement Robustness", ("detailed placement", "legalization", "ntuplace3", "abcdplace")),
    "P7": Topic("P7", "Cross-Domain Risks", ("thermal", "security", "reliability", "backside")),
    "P8": Topic("P8", "Generalization & Transferability", ("cross-design generalization", "benchmark transferability", "robustness")),
}

METHODS: Dict[str, Topic] = {
    "M1": Topic("M1", "Objective Shaping in Placement", ("placement objective", "multi-objective", "cost term")),
    "M2": Topic("M2", "Local Resource-Aware Modeling", ("rudy", "local density", "resource-aware model")),
    "M3": Topic("M3", "Backside Cost/Predictor Modeling", ("backside predictor", "cost model", "delay/power proxy")),
    "M4": Topic("M4", "Constraint-Guided Optimization", ("constrained optimization", "guardrail", "non-regression")),
    "M5": Topic("M5", "A/B + Causal Validation", ("ablation", "causal validation", "paired experiment")),
    "M6": Topic("M6", "Stage-Gated Flow Integration", ("stage checkpoint", "golden resume", "flow gate")),
    "M7": Topic("M7", "Legalization/DP Strategy", ("legalization", "detailed placement", "ntuplace3", "abcdplace")),
}

# Focus priorities for this project.
PRIORITY_SUBPROBLEMS = ("P1", "P2", "P3", "P4", "P6")
PRIORITY_METHODS = ("M1", "M3", "M4", "M5", "M7")


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f, delimiter="\t")]


def as_year(s: str) -> int:
    try:
        return int(s)
    except Exception:
        return 0


def build_query(subproblem: str, method: str, recency_years: int) -> str:
    sp = SUBPROBLEMS[subproblem]
    mt = METHODS[method]
    keys = list(sp.keywords[:2]) + list(mt.keywords[:2]) + ["EDA", "backside"]
    return " ".join(keys + [f"last {recency_years} years"])


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate literature feedback queue from global landscape")
    ap.add_argument("--global-tsv", default=str(GLOBAL_TSV))
    ap.add_argument("--stale-years", type=int, default=3, help="method considered stale if latest year <= current_year-stale_years")
    ap.add_argument("--current-year", type=int, default=2026)
    args = ap.parse_args()

    rows = read_rows(Path(args.global_tsv))
    if not rows:
        print("ERROR: no rows in global landscape")
        return 2

    sub_count = defaultdict(int)
    method_count = defaultdict(int)
    pair_count = defaultdict(int)
    method_years = defaultdict(list)

    for r in rows:
        sp = r.get("primary_subproblem", "")
        mt = r.get("primary_method", "")
        yy = as_year(r.get("year", ""))
        if sp:
            sub_count[sp] += 1
        if mt:
            method_count[mt] += 1
            if yy:
                method_years[mt].append(yy)
        if sp and mt:
            pair_count[(sp, mt)] += 1

    missing_sub = [k for k in SUBPROBLEMS if sub_count[k] == 0]
    missing_method = [k for k in METHODS if method_count[k] == 0]

    sparse_priority_pairs = []
    for sp in PRIORITY_SUBPROBLEMS:
        for mt in PRIORITY_METHODS:
            c = pair_count[(sp, mt)]
            if c == 0:
                sparse_priority_pairs.append((sp, mt, "empty"))
            elif c == 1:
                sparse_priority_pairs.append((sp, mt, "weak"))

    stale_methods = []
    threshold = args.current_year - args.stale_years
    for mt in METHODS:
        years = method_years.get(mt, [])
        latest = max(years) if years else 0
        if latest == 0 or latest <= threshold:
            stale_methods.append((mt, latest))

    # Build queue
    queue_rows = []
    qid = 1
    for sp in missing_sub:
        for mt in PRIORITY_METHODS[:3]:
            queue_rows.append(
                {
                    "queue_id": f"FB{qid:03d}",
                    "priority": "high",
                    "type": "missing_subproblem",
                    "target_subproblem": sp,
                    "target_method": mt,
                    "reason": f"No paper coverage for {sp} in local landscape",
                    "query": build_query(sp, mt, 5),
                    "status": "todo",
                }
            )
            qid += 1

    for mt in missing_method:
        for sp in PRIORITY_SUBPROBLEMS[:3]:
            queue_rows.append(
                {
                    "queue_id": f"FB{qid:03d}",
                    "priority": "high",
                    "type": "missing_method",
                    "target_subproblem": sp,
                    "target_method": mt,
                    "reason": f"No method coverage for {mt} in local landscape",
                    "query": build_query(sp, mt, 5),
                    "status": "todo",
                }
            )
            qid += 1

    for sp, mt, severity in sparse_priority_pairs:
        queue_rows.append(
            {
                "queue_id": f"FB{qid:03d}",
                "priority": "high" if severity == "empty" else "medium",
                "type": "sparse_priority_pair",
                "target_subproblem": sp,
                "target_method": mt,
                "reason": f"Priority pair {sp}+{mt} is {severity} (count={pair_count[(sp, mt)]})",
                "query": build_query(sp, mt, 4 if severity == "empty" else 3),
                "status": "todo",
            }
        )
        qid += 1

    for mt, latest in stale_methods:
        for sp in PRIORITY_SUBPROBLEMS[:2]:
            queue_rows.append(
                {
                    "queue_id": f"FB{qid:03d}",
                    "priority": "medium",
                    "type": "stale_method_followup",
                    "target_subproblem": sp,
                    "target_method": mt,
                    "reason": f"Method {mt} latest local year={latest or 'none'}; needs recent tracking",
                    "query": build_query(sp, mt, 3),
                    "status": "todo",
                }
            )
            qid += 1

    # Deduplicate by query
    seen = set()
    uniq = []
    for r in queue_rows:
        k = (r["target_subproblem"], r["target_method"], r["query"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)

    OUT_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    fields = ["queue_id", "priority", "type", "target_subproblem", "target_method", "reason", "query", "status"]
    with OUT_QUEUE.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=fields)
        w.writeheader()
        for r in uniq:
            w.writerow(r)

    # Markdown report
    lines: List[str] = []
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append("# Literature Feedback Loop (Auto-Synced)")
    lines.append("")
    lines.append(f"- timestamp: `{ts}`")
    lines.append(f"- source_global_landscape: `{Path(args.global_tsv).relative_to(ROOT)}`")
    lines.append(f"- papers_scanned: `{len(rows)}`")
    lines.append(f"- stale_threshold: `latest_year <= {threshold}`")
    lines.append("")

    lines.append("## Coverage Gaps")
    lines.append(f"- missing_subproblems: `{','.join(missing_sub) if missing_sub else 'none'}`")
    lines.append(f"- missing_methods: `{','.join(missing_method) if missing_method else 'none'}`")
    lines.append(f"- sparse_priority_pairs: `{len(sparse_priority_pairs)}`")
    lines.append("")

    lines.append("## Stale Method Watchlist")
    if stale_methods:
        lines.append("| method_id | method | latest_year |")
        lines.append("|---|---|---:|")
        for mt, latest in stale_methods:
            lines.append(f"| {mt} | {METHODS[mt].label} | {latest if latest else 'none'} |")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Targeted Retrieval Queue")
    lines.append(f"- queue_path: `{OUT_QUEUE.relative_to(ROOT)}`")
    lines.append(f"- queue_rows: `{len(uniq)}`")
    lines.append("- top_queries:")
    for r in uniq[:12]:
        lines.append(f"  - [{r['priority']}] {r['target_subproblem']}+{r['target_method']}: {r['query']}")
    lines.append("")

    lines.append("## Suggested Execution")
    lines.append("1. Run `eda-paper-fetch` using top high-priority rows from queue.")
    lines.append("2. Download/summarize new papers, then run `paper_kb_index.py build`.")
    lines.append("3. Re-run this feedback script and compare gap/stale counts.")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote: {OUT_MD}")
    print(f"wrote: {OUT_QUEUE}")
    print(f"missing_subproblems={len(missing_sub)}")
    print(f"missing_methods={len(missing_method)}")
    print(f"sparse_priority_pairs={len(sparse_priority_pairs)}")
    print(f"stale_methods={len(stale_methods)}")
    print(f"queue_rows={len(uniq)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
