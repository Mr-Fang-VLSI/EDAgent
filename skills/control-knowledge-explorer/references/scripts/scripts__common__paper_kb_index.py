#!/usr/bin/env python3
import argparse
import csv
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

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
ROOT = Path(__file__).resolve().parents[2]


def norm_text(s: str) -> str:
    return (s or "").strip().lower()


def tokens(s: str):
    return [t for t in TOKEN_RE.findall(norm_text(s)) if t and t not in STOP]


def expand_tokens(tok_set):
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


def parse_summary(path: Path):
    data = {
        "summary_path": str(path),
        "title": "",
        "authors": "",
        "venue": "",
        "year": "",
        "keywords": "",
        "logic_tags": "",
        "relevance_note": "",
    }
    txt = path.read_text(encoding="utf-8", errors="ignore")
    for line in txt.splitlines():
        l = line.strip()
        if l.lower().startswith("- title:"):
            data["title"] = l.split(":", 1)[1].strip()
        elif l.lower().startswith("- authors:"):
            data["authors"] = l.split(":", 1)[1].strip()
        elif l.lower().startswith("- venue/year:"):
            vy = l.split(":", 1)[1].strip()
            data["venue"] = vy
            ym = re.search(r"(19|20)\d{2}", vy)
            if ym:
                data["year"] = ym.group(0)
        elif l.lower().startswith("- keywords:"):
            data["keywords"] = l.split(":", 1)[1].strip()
        elif l.lower().startswith("- logic_tags:"):
            data["logic_tags"] = l.split(":", 1)[1].strip()
        elif l.lower().startswith("- supports/contradicts/neutral:"):
            data["relevance_note"] = l.split(":", 1)[1].strip()
    return data


def load_manifests(manifest_dir: Path):
    rows = []
    for p in sorted(manifest_dir.glob("*.tsv")):
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for r in reader:
                rr = {k: (v or "").strip() for k, v in r.items()}
                rr["manifest_path"] = str(p)
                rr["paper_id"] = rr.get("paper_id") or slug(rr.get("title", ""))
                rows.append(rr)
    return rows


def build_index(papers_root: Path):
    manifest_dir = papers_root / "manifests"
    summary_dir = papers_root / "summaries"
    index_dir = papers_root / "index"
    index_dir.mkdir(parents=True, exist_ok=True)

    manifest_rows = load_manifests(manifest_dir)
    by_id = {}
    by_title = {}
    for r in manifest_rows:
        pid = r.get("paper_id", "")
        if pid:
            by_id[pid] = r
        t = norm_text(r.get("title", ""))
        if t:
            by_title[t] = r

    entries = {}
    for r in manifest_rows:
        pid = r.get("paper_id") or slug(r.get("title", ""))
        entries[pid] = dict(r)

    for sp in sorted(summary_dir.glob("*.summary.md")):
        sd = parse_summary(sp)
        title_key = norm_text(sd.get("title", ""))
        pid = ""
        if title_key and title_key in by_title:
            pid = by_title[title_key].get("paper_id", "")
        if not pid:
            pid = slug(sd.get("title", "") or sp.stem.replace(".summary", ""))
        cur = entries.get(pid, {})
        cur.update(sd)
        cur["paper_id"] = pid
        entries[pid] = cur

    for pid, e in entries.items():
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
        e["text_blob"] = blob
        tok = set(tokens(blob))
        e["tokens"] = sorted(tok)
        e["tokens_expanded"] = sorted(expand_tokens(tok))

    json_path = index_dir / "paper_index.json"
    tsv_path = index_dir / "paper_index.tsv"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(
            {"entries": list(entries.values())},
            f,
            ensure_ascii=False,
            indent=2,
        )

    fields = [
        "paper_id",
        "title",
        "authors",
        "venue",
        "year",
        "status",
        "url",
        "doi_or_arxiv",
        "local_pdf_path",
        "summary_path",
        "keywords",
        "logic_tags",
        "relevance_note",
        "manifest_path",
    ]
    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=fields)
        w.writeheader()
        for e in entries.values():
            w.writerow({k: e.get(k, "") for k in fields})

    print(f"wrote: {json_path}")
    print(f"wrote: {tsv_path}")
    print(f"entries: {len(entries)}")


def sync_landscape() -> int:
    script = ROOT / "scripts" / "common" / "paper_landscape_sync.py"
    if not script.exists():
        print(f"WARN: landscape sync script missing: {script}")
        return 1
    try:
        subprocess.run(["python3", str(script), "build"], check=True)
        print("landscape_sync: PASS")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"WARN: landscape_sync failed (exit={e.returncode})")
        return e.returncode


def sync_feedback() -> int:
    script = ROOT / "scripts" / "common" / "paper_landscape_feedback.py"
    if not script.exists():
        print(f"WARN: feedback sync script missing: {script}")
        return 1
    try:
        subprocess.run(["python3", str(script)], check=True)
        print("feedback_sync: PASS")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"WARN: feedback_sync failed (exit={e.returncode})")
        return e.returncode


def load_index(index_json: Path):
    with index_json.open("r", encoding="utf-8") as f:
        return json.load(f).get("entries", [])


def score_keyword(entry, q_tokens):
    tset = set(entry.get("tokens", []))
    title_toks = set(tokens(entry.get("title", "")))
    key_toks = set(tokens(entry.get("keywords", "")))
    hit = 0.0
    for t in q_tokens:
        if t in tset:
            hit += 1.0
        if t in title_toks:
            hit += 1.5
        if t in key_toks:
            hit += 1.2
    return hit


def logic_to_rpn(expr: str):
    toks = [t for t in LOGIC_TOKEN_RE.findall(expr) if t.strip()]
    out = []
    op = []
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


def eval_logic_rpn(rpn, token_set):
    st = []
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


def score_semantic(entry, q_tokens):
    q_exp = expand_tokens(set(q_tokens))
    d_exp = set(entry.get("tokens_expanded", []))
    if not q_exp or not d_exp:
        return 0.0
    inter = len(q_exp & d_exp)
    union = len(q_exp | d_exp)
    return inter / union if union else 0.0


def run_query(index_json: Path, mode: str, q: str, top_k: int, out_dir: Path):
    entries = load_index(index_json)
    q_tokens = tokens(q)
    if not q_tokens and mode != "logic":
        print("ERROR: empty query tokens", file=sys.stderr)
        return 2

    rpn = logic_to_rpn(q) if mode == "logic" else None
    scored = []

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
            score = 0.6 * kw + 0.4 * sem
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

    out_dir.mkdir(parents=True, exist_ok=True)
    out_tsv = out_dir / "query_last.tsv"
    fields = [
        "rank",
        "score",
        "paper_id",
        "title",
        "year",
        "venue",
        "status",
        "doi_or_arxiv",
        "url",
        "local_pdf_path",
        "summary_path",
        "keywords",
        "logic_tags",
    ]
    with out_tsv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=fields)
        w.writeheader()
        for i, (score, e) in enumerate(top, start=1):
            row = {k: e.get(k, "") for k in fields}
            row["rank"] = i
            row["score"] = f"{score:.6f}"
            w.writerow(row)

    print(f"mode={mode}")
    print(f"query={q}")
    print(f"hits={len(top)}")
    print(f"wrote: {out_tsv}")
    for i, (score, e) in enumerate(top[:10], start=1):
        print(f"{i:2d}. {score:.4f} | {e.get('paper_id','')} | {e.get('title','')}")
    return 0


def main():
    p = argparse.ArgumentParser(description="Paper KB index builder/query tool")
    sub = p.add_subparsers(dest="cmd", required=True)

    pb = sub.add_parser("build", help="build paper index")
    pb.add_argument("--papers-root", default="docs/papers")
    pb.add_argument(
        "--no-sync-landscape",
        action="store_true",
        help="disable automatic problem/method landscape sync after index build",
    )
    pb.add_argument(
        "--no-sync-feedback",
        action="store_true",
        help="disable automatic literature feedback queue sync after index build",
    )

    pq = sub.add_parser("query", help="query paper index")
    pq.add_argument("--index-json", default="docs/papers/index/paper_index.json")
    pq.add_argument("--mode", choices=["keyword", "logic", "semantic", "hybrid"], default="hybrid")
    pq.add_argument("--q", required=True, help="query string")
    pq.add_argument("--top-k", type=int, default=20)
    pq.add_argument("--out-dir", default="docs/papers/index")

    args = p.parse_args()
    if args.cmd == "build":
        build_index(Path(args.papers_root))
        if not args.no_sync_landscape:
            sync_landscape()
        if not args.no_sync_feedback:
            sync_feedback()
        return 0
    if args.cmd == "query":
        return run_query(
            Path(args.index_json),
            args.mode,
            args.q,
            args.top_k,
            Path(args.out_dir),
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
