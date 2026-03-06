#!/usr/bin/env python3
"""Build and refresh paper landscapes:
- problem landscape
- method landscape
- global research landscape (subproblem-method-effect-group-paper)
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
SUMMARY_DIR = ROOT / "docs" / "papers" / "summaries"
MANIFEST_DIR = ROOT / "docs" / "papers" / "manifests"
OUT_DIR = ROOT / "docs" / "knowledge_base"
INDEX_DIR = OUT_DIR / "index"

PROBLEM_OUT = OUT_DIR / "95_PROBLEM_LANDSCAPE.md"
METHOD_OUT = OUT_DIR / "96_METHOD_LANDSCAPE.md"
GLOBAL_OUT = OUT_DIR / "97_GLOBAL_RESEARCH_LANDSCAPE.md"
GRAPH_OUT = INDEX_DIR / "landscape_graph.json"
MATRIX_OUT = INDEX_DIR / "landscape_problem_method_matrix.tsv"
GLOBAL_TSV_OUT = INDEX_DIR / "global_research_landscape.tsv"

ANNOTATION_TSV = MANIFEST_DIR / "landscape_annotations.tsv"


@dataclass(frozen=True)
class Theme:
    key: str
    label: str
    kind: str
    description: str
    patterns: Tuple[str, ...]


PROBLEM_THEMES: Tuple[Theme, ...] = (
    Theme("P1", "Routing Capacity & Congestion", "problem", "Routing demand exceeds available resources, causing overflow/hotspots.", ("congestion", "overflow", "routing demand", "capacity", "hotspot", "crowding")),
    Theme("P2", "Backside Resource Allocation", "problem", "Need principled front-vs-back net assignment under finite backside resources.", ("backside", "frontside", "bm1", "bm2", "dual-side", "assignment", "crossover")),
    Theme("P3", "Timing Closure Sensitivity", "problem", "QoR highly sensitive to critical-path and clock-data interaction under placement/routing changes.", ("timing", "critical path", "wns", "tns", "latency", "clock")),
    Theme("P4", "Dynamic Power Reduction Under Constraints", "problem", "Lower dynamic power without area/timing regression.", ("dynamic power", "switching", "power reduction", "activity", "capacitance")),
    Theme("P5", "Via/TSV & Interconnect Constraints", "problem", "nTSV/via and interconnect parasitics constrain backside benefits.", ("ntsv", "tsv", "via", "parasitic", "resistance", "capacitance")),
    Theme("P6", "Legality & Detailed Placement Robustness", "problem", "Global-placement gains may vanish if legalization/detailed placement is unstable.", ("legal", "legalization", "detailed placement", "displacement", "overlap")),
    Theme("P7", "Cross-Domain Risks", "problem", "Thermal/security/reliability effects can veto aggressive backside usage.", ("thermal", "security", "side-channel", "reliability", "ir-drop", "noise")),
    Theme("P8", "Generalization & Transferability", "problem", "Benchmark improvements may not transfer across designs/flows.", ("benchmark", "transfer", "generalization", "validity", "threat", "runtime")),
)

METHOD_THEMES: Tuple[Theme, ...] = (
    Theme("M1", "Objective Shaping in Placement", "method", "Modify objective with domain-aware terms instead of pure HPWL.", ("objective", "penalty", "hpwl", "cost", "density term", "lambda")),
    Theme("M2", "Local Resource-Aware Modeling", "method", "Use local density/capacity/congestion proxies to guide optimization.", ("local density", "per-bin", "rudy", "congestion estimation", "capacity-aware")),
    Theme("M3", "Backside Cost/Predictor Modeling", "method", "Build front-vs-back delay/power proxy models with stability gates.", ("predictor", "model", "regression", "cost model", "shadow mode", "gate")),
    Theme("M4", "Constraint-Guided Optimization", "method", "Use hard/soft constraints (timing, risk budget, policy lock) to prevent invalid wins.", ("constraint", "guardrail", "risk budget", "policy", "lock", "non-regression")),
    Theme("M5", "A/B + Causal Validation", "method", "Use paired experiments/ablation to isolate mechanism and avoid confounding.", ("a/b", "ablation", "paired", "causal", "control", "baseline")),
    Theme("M6", "Stage-Gated Flow Integration", "method", "Integrate method through reproducible stage checkpoints and promotion gates.", ("checkpoint", "stage", "golden", "resume", "promotion", "preflight")),
    Theme("M7", "Legalization/DP Strategy", "method", "Use explicit detailed placement/legalization strategy (e.g., NTUplace3/ABCDPlace fallback).", ("ntuplace3", "abcdplace", "detailed placement", "legalization", "failover")),
)

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
META_RE = re.compile(r"^-\s*(title|authors|venue/year|local_pdf):\s*(.*)\s*$", re.M | re.I)
YEAR_RE = re.compile(r"(19|20)\d{2}")


def norm(s: str) -> str:
    return (s or "").strip().lower()


def slug(s: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "_", norm(s)).strip("_")
    return text or "unknown"


def key_to_label(themes: Tuple[Theme, ...]) -> Dict[str, str]:
    return {t.key: t.label for t in themes}


def parse_first_author(authors: str) -> str:
    if not authors:
        return "unknown-group"
    primary = re.split(r";|,| and ", authors, maxsplit=1)[0].strip()
    if not primary:
        return "unknown-group"
    if "et al" in primary.lower():
        return primary
    return f"{primary} et al."


def parse_effect_snippet(evidence: str) -> str:
    for line in evidence.splitlines():
        s = line.strip()
        if s.startswith("- result-"):
            val = re.sub(r"^-\s*result-[0-9]+\s*\([^)]*\)\s*", "", s)
            val = re.sub(r"\[[^\]]+\]", "", val).strip(" :")
            return val[:180] if val else ""
    lines = [x.strip() for x in evidence.splitlines() if x.strip()]
    if lines:
        return lines[0][:180]
    return ""


def load_manifest_map() -> Dict[str, Dict[str, str]]:
    by_title: Dict[str, Dict[str, str]] = {}
    for p in sorted(MANIFEST_DIR.glob("*.paper_manifest.tsv")):
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                title = norm(row.get("title", ""))
                if not title:
                    continue
                by_title[title] = {k: (v or "").strip() for k, v in row.items()}
    return by_title


def load_annotations() -> Dict[str, Dict[str, str]]:
    out: Dict[str, Dict[str, str]] = {}
    if not ANNOTATION_TSV.exists():
        return out
    with ANNOTATION_TSV.open("r", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pid = (row.get("paper_id") or "").strip()
            if not pid:
                continue
            out[pid] = {k: (v or "").strip() for k, v in row.items()}
    return out


def write_annotations(papers: List[Dict[str, str]], existing: Dict[str, Dict[str, str]]) -> None:
    cols = [
        "paper_id",
        "research_group",
        "organization_hint",
        "primary_subproblem",
        "primary_method",
        "key_effect_summary",
        "key_metric",
        "curation_note",
    ]
    rows = []
    for p in papers:
        pid = p["paper_id"]
        old = existing.get(pid, {})
        rows.append(
            {
                "paper_id": pid,
                "research_group": old.get("research_group", p.get("research_group_guess", "")),
                "organization_hint": old.get("organization_hint", ""),
                "primary_subproblem": old.get("primary_subproblem", p.get("primary_subproblem_guess", "")),
                "primary_method": old.get("primary_method", p.get("primary_method_guess", "")),
                "key_effect_summary": old.get("key_effect_summary", p.get("key_effect_guess", "")),
                "key_metric": old.get("key_metric", ""),
                "curation_note": old.get("curation_note", ""),
            }
        )
    rows.sort(key=lambda r: r["paper_id"])
    ANNOTATION_TSV.parent.mkdir(parents=True, exist_ok=True)
    with ANNOTATION_TSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_summary(path: Path, manifest_map: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    meta = {"title": path.stem.replace(".summary", ""), "authors": "", "venue/year": "", "local_pdf": ""}
    for m in META_RE.finditer(text):
        meta[m.group(1).lower()] = m.group(2).strip()

    sections: Dict[str, str] = {}
    matches = list(SECTION_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[m.group(1).strip().lower()] = text[start:end].strip()

    title = meta.get("title", "")
    mrow = manifest_map.get(norm(title), {})
    paper_id = mrow.get("paper_id") or slug(title)
    venue_year = meta.get("venue/year", "")
    year_m = YEAR_RE.search(venue_year)

    return {
        "paper_id": paper_id,
        "path": str(path.relative_to(ROOT)),
        "title": title,
        "authors": meta.get("authors", ""),
        "venue_year": venue_year,
        "venue": mrow.get("venue", ""),
        "year": mrow.get("year", "") or (year_m.group(0) if year_m else ""),
        "problem": sections.get("problem and context", ""),
        "method": sections.get("method", ""),
        "evidence": sections.get("evidence", ""),
        "limits": sections.get("limits and threats to validity", ""),
        "relevance": sections.get("relevance to current project", ""),
        "next_step": sections.get("actionable next step", ""),
        "full_text": text,
    }


def match_themes(text: str, themes: Tuple[Theme, ...]) -> List[str]:
    t = norm(text)
    hits = []
    for th in themes:
        if any(p in t for p in th.patterns):
            hits.append(th.key)
    return hits


def build_landscape() -> Dict[str, object]:
    manifest_map = load_manifest_map()
    papers = []
    for p in sorted(SUMMARY_DIR.glob("*.summary.md")):
        paper = read_summary(p, manifest_map)
        problem_blob = "\n".join([paper["problem"], paper["limits"], paper["relevance"], paper["next_step"], paper["full_text"][:2500]])
        method_blob = "\n".join([paper["method"], paper["evidence"], paper["relevance"], paper["next_step"], paper["full_text"][:2500]])
        paper["problem_tags"] = match_themes(problem_blob, PROBLEM_THEMES)
        paper["method_tags"] = match_themes(method_blob, METHOD_THEMES)
        paper["research_group_guess"] = parse_first_author(paper["authors"])
        paper["primary_subproblem_guess"] = paper["problem_tags"][0] if paper["problem_tags"] else ""
        paper["primary_method_guess"] = paper["method_tags"][0] if paper["method_tags"] else ""
        paper["key_effect_guess"] = parse_effect_snippet(paper["evidence"])
        papers.append(paper)

    annotations = load_annotations()
    write_annotations(papers, annotations)
    annotations = load_annotations()

    p2papers: Dict[str, List[str]] = defaultdict(list)
    m2papers: Dict[str, List[str]] = defaultdict(list)
    pair_count: Dict[Tuple[str, str], int] = defaultdict(int)

    for p in papers:
        title = p["title"]
        for pt in p["problem_tags"]:
            p2papers[pt].append(title)
        for mt in p["method_tags"]:
            m2papers[mt].append(title)
        for pt in p["problem_tags"]:
            for mt in p["method_tags"]:
                pair_count[(pt, mt)] += 1

        ann = annotations.get(p["paper_id"], {})
        p["research_group"] = ann.get("research_group") or p["research_group_guess"]
        p["primary_subproblem"] = ann.get("primary_subproblem") or p["primary_subproblem_guess"]
        p["primary_method"] = ann.get("primary_method") or p["primary_method_guess"]
        p["key_effect_summary"] = ann.get("key_effect_summary") or p["key_effect_guess"]
        p["key_metric"] = ann.get("key_metric", "")

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "paper_count": len(papers),
        "papers": papers,
        "problem_map": {k: sorted(v) for k, v in p2papers.items()},
        "method_map": {k: sorted(v) for k, v in m2papers.items()},
        "pair_count": {f"{k[0]}::{k[1]}": v for k, v in sorted(pair_count.items())},
    }


def write_problem_md(data: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# Problem Landscape (Auto-Synced)")
    lines.append("")
    lines.append(f"- last_sync: `{data['timestamp']}`")
    lines.append(f"- source: `docs/papers/summaries/*.summary.md`")
    lines.append(f"- papers_scanned: `{data['paper_count']}`")
    lines.append("")
    lines.append("## Landscape Nodes")
    lines.append("| id | problem | evidence_papers | linked_methods |")
    lines.append("|---|---|---:|---|")

    pair_count = data["pair_count"]
    for th in PROBLEM_THEMES:
        papers = data["problem_map"].get(th.key, [])
        linked_methods = []
        for mt in METHOD_THEMES:
            if pair_count.get(f"{th.key}::{mt.key}", 0) > 0:
                linked_methods.append(mt.key)
        lines.append(f"| {th.key} | {th.label} | {len(papers)} | {','.join(linked_methods) if linked_methods else '-'} |")

    lines.append("")
    lines.append("## Node Details")
    for th in PROBLEM_THEMES:
        papers = data["problem_map"].get(th.key, [])
        lines.append(f"### {th.key} {th.label}")
        lines.append(f"- description: {th.description}")
        lines.append(f"- matched_papers: `{len(papers)}`")
        if papers:
            lines.append("- examples:")
            for t in papers[:10]:
                lines.append(f"  - {t}")
        else:
            lines.append("- examples: none")
        lines.append("")

    PROBLEM_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_method_md(data: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# Method Landscape (Auto-Synced)")
    lines.append("")
    lines.append(f"- last_sync: `{data['timestamp']}`")
    lines.append(f"- source: `docs/papers/summaries/*.summary.md`")
    lines.append(f"- papers_scanned: `{data['paper_count']}`")
    lines.append("")
    lines.append("## Landscape Nodes")
    lines.append("| id | method family | evidence_papers | addresses_problems |")
    lines.append("|---|---|---:|---|")

    pair_count = data["pair_count"]
    for th in METHOD_THEMES:
        papers = data["method_map"].get(th.key, [])
        linked_problems = []
        for pt in PROBLEM_THEMES:
            if pair_count.get(f"{pt.key}::{th.key}", 0) > 0:
                linked_problems.append(pt.key)
        lines.append(f"| {th.key} | {th.label} | {len(papers)} | {','.join(linked_problems) if linked_problems else '-'} |")

    lines.append("")
    lines.append("## Node Details")
    for th in METHOD_THEMES:
        papers = data["method_map"].get(th.key, [])
        lines.append(f"### {th.key} {th.label}")
        lines.append(f"- description: {th.description}")
        lines.append(f"- matched_papers: `{len(papers)}`")
        if papers:
            lines.append("- examples:")
            for t in papers[:10]:
                lines.append(f"  - {t}")
        else:
            lines.append("- examples: none")
        lines.append("")

    METHOD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_global_md(data: Dict[str, object]) -> None:
    p_labels = key_to_label(PROBLEM_THEMES)
    m_labels = key_to_label(METHOD_THEMES)

    by_subproblem = defaultdict(int)
    by_method = defaultdict(int)
    by_group = defaultdict(int)

    rows = []
    for p in data["papers"]:
        sp = p.get("primary_subproblem", "")
        mt = p.get("primary_method", "")
        gp = p.get("research_group", "")
        by_subproblem[sp] += 1
        by_method[mt] += 1
        by_group[gp] += 1
        rows.append(
            {
                "paper_id": p.get("paper_id", ""),
                "title": p.get("title", ""),
                "year": p.get("year", ""),
                "venue": p.get("venue", "") or p.get("venue_year", ""),
                "research_group": gp,
                "primary_subproblem": sp,
                "primary_subproblem_label": p_labels.get(sp, sp),
                "primary_method": mt,
                "primary_method_label": m_labels.get(mt, mt),
                "key_effect_summary": p.get("key_effect_summary", ""),
                "key_metric": p.get("key_metric", ""),
                "summary_path": p.get("path", ""),
            }
        )
    rows.sort(key=lambda r: (r["primary_subproblem"], r["primary_method"], r["year"], r["title"]))

    lines: List[str] = []
    lines.append("# Global Research Landscape (Auto-Synced)")
    lines.append("")
    lines.append(f"- last_sync: `{data['timestamp']}`")
    lines.append(f"- papers_scanned: `{data['paper_count']}`")
    lines.append(f"- annotation_table: `{ANNOTATION_TSV.relative_to(ROOT)}`")
    lines.append("")

    lines.append("## Global View")
    lines.append("### Subproblem Coverage")
    lines.append("| subproblem_id | subproblem | paper_count |")
    lines.append("|---|---|---:|")
    for k, c in sorted(by_subproblem.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| {k} | {p_labels.get(k, k)} | {c} |")
    lines.append("")

    lines.append("### Method Coverage")
    lines.append("| method_id | method | paper_count |")
    lines.append("|---|---|---:|")
    for k, c in sorted(by_method.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| {k} | {m_labels.get(k, k)} | {c} |")
    lines.append("")

    lines.append("### Group Coverage")
    lines.append("| research_group | paper_count |")
    lines.append("|---|---:|")
    for k, c in sorted(by_group.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| {k} | {c} |")
    lines.append("")

    lines.append("## Paper-Level Mapping")
    lines.append("| subproblem | method | effect_summary | group | paper | year | venue | paper_id |")
    lines.append("|---|---|---|---|---|---:|---|---|")
    for r in rows:
        lines.append(
            "| {sp} | {mt} | {ef} | {gp} | {tt} | {yy} | {vv} | `{pid}` |".format(
                sp=r["primary_subproblem_label"],
                mt=r["primary_method_label"],
                ef=(r["key_effect_summary"] or "").replace("|", "/"),
                gp=(r["research_group"] or "").replace("|", "/"),
                tt=(r["title"] or "").replace("|", "/"),
                yy=r["year"] or "",
                vv=(r["venue"] or "").replace("|", "/"),
                pid=r["paper_id"],
            )
        )

    lines.append("")
    lines.append("## Curation Notes")
    lines.append("- `research_group` / `primary_subproblem` / `primary_method` / `key_effect_summary` can be manually edited in annotation table.")
    lines.append("- If annotation is empty, this doc uses auto-inferred values from summary text.")

    GLOBAL_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    fields = [
        "paper_id",
        "title",
        "year",
        "venue",
        "research_group",
        "primary_subproblem",
        "primary_subproblem_label",
        "primary_method",
        "primary_method_label",
        "key_effect_summary",
        "key_metric",
        "summary_path",
    ]
    with GLOBAL_TSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def write_matrix_tsv(data: Dict[str, object]) -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["problem_id\tmethod_id\tcooccurrence_count"]
    for p in PROBLEM_THEMES:
        for m in METHOD_THEMES:
            c = data["pair_count"].get(f"{p.key}::{m.key}", 0)
            lines.append(f"{p.key}\t{m.key}\t{c}")
    MATRIX_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_graph_json(data: Dict[str, object]) -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    nodes = []
    for p in PROBLEM_THEMES:
        nodes.append({"id": p.key, "type": "problem", "label": p.label, "description": p.description})
    for m in METHOD_THEMES:
        nodes.append({"id": m.key, "type": "method", "label": m.label, "description": m.description})

    edges = []
    for p in PROBLEM_THEMES:
        for m in METHOD_THEMES:
            c = data["pair_count"].get(f"{p.key}::{m.key}", 0)
            if c > 0:
                edges.append({"source": p.key, "target": m.key, "weight": c})

    payload = {
        "timestamp": data["timestamp"],
        "paper_count": data["paper_count"],
        "nodes": nodes,
        "edges": edges,
    }
    GRAPH_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync problem/method/global landscape from local summaries")
    ap.add_argument("build", nargs="?", default="build")
    args = ap.parse_args()
    _ = args

    data = build_landscape()
    write_problem_md(data)
    write_method_md(data)
    write_global_md(data)
    write_matrix_tsv(data)
    write_graph_json(data)

    print(f"wrote: {PROBLEM_OUT}")
    print(f"wrote: {METHOD_OUT}")
    print(f"wrote: {GLOBAL_OUT}")
    print(f"wrote: {GLOBAL_TSV_OUT}")
    print(f"wrote: {MATRIX_OUT}")
    print(f"wrote: {GRAPH_OUT}")
    print(f"wrote: {ANNOTATION_TSV}")
    print(f"papers_scanned: {data['paper_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
