#!/usr/bin/env python3
"""Unified local retrieval for knowledge-base docs and paper evidence index."""

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[2]
KB_DIR = ROOT / "docs" / "knowledge_base"
KB_INDEX_DIR = KB_DIR / "index"
KB_INDEX_JSON = KB_INDEX_DIR / "kb_index.json"
KB_INDEX_TSV = KB_INDEX_DIR / "kb_index.tsv"
PAPER_INDEX_JSON = ROOT / "docs" / "papers" / "index" / "paper_index.json"
QUERY_OUT = KB_INDEX_DIR / "query_last.tsv"

TOKEN_RE = re.compile(r"[a-z0-9_]+")
LOGIC_TOKEN_RE = re.compile(r"\(|\)|\bAND\b|\bOR\b|\bNOT\b|[A-Za-z0-9_:-]+")
STOP = {
    "the", "a", "an", "of", "to", "for", "in", "on", "with", "and", "or", "by",
    "from", "at", "is", "are", "be", "as", "that", "this", "we", "our", "using",
}
SYNONYMS = {
    "backside": {"bspdn", "back", "bm1", "bm2", "bpr"},
    "frontside": {"front", "m1", "m2", "m3", "m4", "m5"},
    "clock": {"cts", "clocktree", "skew", "latency"},
    "signal": {"data", "net", "timingpath"},
    "congestion": {"overflow", "crowding", "hotspot"},
    "capacity": {"resource", "limit", "budget"},
    "ntsv": {"tsv", "via"},
    "delay": {"tau", "latency", "arrival"},
    "cost": {"objective", "score", "penalty"},
    "placement": {"replace", "globalplace", "legalization"},
    "routing": {"route", "detailroute", "globalroute"},
}


def norm_text(s: str) -> str:
    return (s or "").strip().lower()


def tokens(s: str) -> List[str]:
    return [t for t in TOKEN_RE.findall(norm_text(s)) if t and t not in STOP]


def expand_tokens(tok_set: Set[str]) -> Set[str]:
    out = set(tok_set)
    reverse = defaultdict(set)
    for k, vals in SYNONYMS.items():
        for v in vals:
            reverse[v].add(k)
    for t in list(tok_set):
        if t in SYNONYMS:
            out.update(SYNONYMS[t])
        if t in reverse:
            out.update(reverse[t])
    return out


def slug(s: str) -> str:
    ts = tokens(s)
    return "_".join(ts[:12]) if ts else "unknown"


def parse_markdown_doc(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    title = ""
    tag_line = ""
    for line in text.splitlines()[:80]:
        l = line.strip()
        if not title and l.startswith("#"):
            title = re.sub(r"^#+\s*", "", l)
        if l.lower().startswith("tags:"):
            tag_line = l.split(":", 1)[1].strip()
    doc_id = slug(title or path.stem)
    blob = " ".join([title, tag_line, text[:8000]])
    tok = set(tokens(blob))
    return {
        "entry_id": doc_id,
        "source": "kb",
        "title": title or path.stem,
        "path": str(path.relative_to(ROOT)),
        "year": "",
        "venue": "",
        "status": "local_doc",
        "keywords": tag_line,
        "text_blob": blob,
        "tokens": sorted(tok),
        "tokens_expanded": sorted(expand_tokens(tok)),
    }


def build_kb_index(include_templates: bool) -> int:
    KB_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    for p in sorted(KB_DIR.rglob("*.md")):
        rel = p.relative_to(KB_DIR).as_posix()
        if "/index/" in rel:
            continue
        if (not include_templates) and rel.startswith("templates/"):
            continue
        entries.append(parse_markdown_doc(p))

    with KB_INDEX_JSON.open("w", encoding="utf-8") as f:
        json.dump({"entries": entries}, f, ensure_ascii=False, indent=2)

    with KB_INDEX_TSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            delimiter="\t",
            fieldnames=["entry_id", "source", "title", "path", "status", "keywords"],
        )
        w.writeheader()
        for e in entries:
            w.writerow({k: e.get(k, "") for k in ["entry_id", "source", "title", "path", "status", "keywords"]})

    print(f"wrote: {KB_INDEX_JSON}")
    print(f"wrote: {KB_INDEX_TSV}")
    print(f"entries: {len(entries)}")
    return 0


def load_entries(source: str) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    if source in {"all", "kb"}:
        if not KB_INDEX_JSON.exists():
            raise FileNotFoundError(f"missing kb index: {KB_INDEX_JSON}; run build first")
        with KB_INDEX_JSON.open("r", encoding="utf-8") as f:
            out.extend(json.load(f).get("entries", []))

    if source in {"all", "paper"}:
        if not PAPER_INDEX_JSON.exists():
            raise FileNotFoundError(f"missing paper index: {PAPER_INDEX_JSON}; run paper_kb_index build first")
        with PAPER_INDEX_JSON.open("r", encoding="utf-8") as f:
            for e in json.load(f).get("entries", []):
                blob = " ".join(
                    [
                        e.get("title", ""),
                        e.get("authors", ""),
                        e.get("venue", ""),
                        e.get("keywords", ""),
                        e.get("logic_tags", ""),
                        e.get("relevance_note", ""),
                        e.get("status", ""),
                    ]
                )
                tok = set(tokens(blob))
                out.append(
                    {
                        "entry_id": e.get("paper_id", slug(e.get("title", ""))),
                        "source": "paper",
                        "title": e.get("title", ""),
                        "path": e.get("summary_path", "") or e.get("local_pdf_path", ""),
                        "year": e.get("year", ""),
                        "venue": e.get("venue", ""),
                        "status": e.get("status", ""),
                        "keywords": e.get("keywords", ""),
                        "text_blob": blob,
                        "tokens": sorted(tok),
                        "tokens_expanded": sorted(expand_tokens(tok)),
                    }
                )
    return out


def score_keyword(entry: Dict[str, object], q_tokens: List[str]) -> float:
    tset = set(entry.get("tokens", []))
    title_toks = set(tokens(str(entry.get("title", ""))))
    key_toks = set(tokens(str(entry.get("keywords", ""))))
    hit = 0.0
    for t in q_tokens:
        if t in tset:
            hit += 1.0
        if t in title_toks:
            hit += 1.4
        if t in key_toks:
            hit += 1.1
    return hit


def score_semantic(entry: Dict[str, object], q_tokens: List[str]) -> float:
    q_exp = expand_tokens(set(q_tokens))
    d_exp = set(entry.get("tokens_expanded", []))
    if not q_exp or not d_exp:
        return 0.0
    inter = len(q_exp & d_exp)
    union = len(q_exp | d_exp)
    return inter / union if union else 0.0


def logic_to_rpn(expr: str) -> List[str]:
    toks = [t for t in LOGIC_TOKEN_RE.findall(expr) if t.strip()]
    out: List[str] = []
    op: List[str] = []
    prec = {"NOT": 3, "AND": 2, "OR": 1}
    for t in toks:
        tu = t.upper()
        if tu in ("AND", "OR", "NOT"):
            while op and op[-1] != "(" and prec.get(op[-1], 0) >= prec[tu]:
                out.append(op.pop())
            op.append(tu)
        elif t == "(":
            op.append(t)
        elif t == ")":
            while op and op[-1] != "(":
                out.append(op.pop())
            if op and op[-1] == "(":
                op.pop()
        else:
            out.append(norm_text(t))
    while op:
        out.append(op.pop())
    return out


def eval_logic_rpn(rpn: List[str], token_set: Set[str]) -> bool:
    st: List[bool] = []
    for t in rpn:
        if t == "NOT":
            a = bool(st.pop()) if st else False
            st.append(not a)
        elif t in ("AND", "OR"):
            b = bool(st.pop()) if st else False
            a = bool(st.pop()) if st else False
            st.append(a and b if t == "AND" else a or b)
        else:
            st.append(t in token_set)
    return bool(st[-1]) if st else False


def run_query(source: str, mode: str, q: str, top_k: int, output: Path) -> int:
    try:
        entries = load_entries(source)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    q_tokens = tokens(q)
    if not q_tokens and mode != "logic":
        print("ERROR: empty query tokens", file=sys.stderr)
        return 2

    rpn = logic_to_rpn(q) if mode == "logic" else None
    scored: List[Tuple[float, Dict[str, object]]] = []

    for e in entries:
        tset = set(e.get("tokens", []))
        kw = score_keyword(e, q_tokens)
        sem = score_semantic(e, q_tokens)
        logic_pass = eval_logic_rpn(rpn, tset) if rpn else True

        if mode == "keyword":
            score = kw
        elif mode == "semantic":
            score = sem
        elif mode == "logic":
            score = kw if logic_pass else 0.0
        elif mode == "hybrid":
            score = 0.65 * kw + 0.35 * sem
        else:
            print(f"ERROR: unknown mode={mode}", file=sys.stderr)
            return 2

        if mode == "logic" and not logic_pass:
            continue
        if score <= 0:
            continue
        scored.append((score, e))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "rank",
        "score",
        "source",
        "entry_id",
        "title",
        "year",
        "venue",
        "status",
        "path",
        "keywords",
    ]
    with output.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=fields)
        w.writeheader()
        for i, (score, e) in enumerate(top, start=1):
            w.writerow(
                {
                    "rank": i,
                    "score": f"{score:.6f}",
                    "source": e.get("source", ""),
                    "entry_id": e.get("entry_id", ""),
                    "title": e.get("title", ""),
                    "year": e.get("year", ""),
                    "venue": e.get("venue", ""),
                    "status": e.get("status", ""),
                    "path": e.get("path", ""),
                    "keywords": e.get("keywords", ""),
                }
            )

    print(f"wrote: {output}")
    print(f"hits: {len(top)} / {len(scored)}")
    for i, (score, e) in enumerate(top[:10], start=1):
        print(f"[{i}] {score:.4f} | {e.get('source')} | {e.get('title')}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Unified query for local knowledge base and paper index")
    sub = p.add_subparsers(dest="cmd")
    sub.required = True

    pb = sub.add_parser("build", help="build knowledge-base index")
    pb.add_argument("--include-templates", action="store_true", help="include docs/knowledge_base/templates")

    pq = sub.add_parser("query", help="query across kb/papers")
    pq.add_argument("--source", choices=["all", "kb", "paper"], default="all")
    pq.add_argument("--mode", choices=["keyword", "semantic", "hybrid", "logic"], default="hybrid")
    pq.add_argument("--query", required=True)
    pq.add_argument("--top-k", type=int, default=20)
    pq.add_argument("--out", default=str(QUERY_OUT))
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.cmd == "build":
        return build_kb_index(include_templates=args.include_templates)
    if args.cmd == "query":
        return run_query(args.source, args.mode, args.query, args.top_k, Path(args.out))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
