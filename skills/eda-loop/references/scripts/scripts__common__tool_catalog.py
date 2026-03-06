#!/usr/bin/env python3
"""Build and query a local catalog of tools/flows/scripts.

Usage:
  python3 scripts/common/tool_catalog.py build
  python3 scripts/common/tool_catalog.py query cts route --type flow_stage
"""

import argparse
import csv
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
OUT_DIR = ROOT / "docs" / "tool_registry"
OUT_TSV = OUT_DIR / "tool_catalog.tsv"
OUT_MD = OUT_DIR / "tool_catalog.md"
META_TSV = OUT_DIR / "tool_metadata.tsv"

SCAN_EXTS = {".sh", ".py", ".tcl", ".md", ".yaml", ".yml"}
IGNORE_DIRS = {"__pycache__", ".git"}

CATALOG_FIELDS = [
    "tool_id",
    "type",
    "lifecycle",
    "version",
    "owner",
    "domain",
    "stage",
    "path",
    "lang",
    "executable",
    "summary",
    "tags",
    "input_contract",
    "output_contract",
    "validator",
    "last_verified",
    "evidence_path",
    "replacement_tool_id",
    "command_hint",
]


@dataclass
class Entry:
    tool_id: str
    tool_type: str
    lifecycle: str
    version: str
    owner: str
    domain: str
    stage: str
    path: str
    lang: str
    executable: int
    summary: str
    tags: str
    input_contract: str
    output_contract: str
    validator: str
    last_verified: str
    evidence_path: str
    replacement_tool_id: str
    command_hint: str


def slugify(text: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return out or "tool"


def detect_type(rel: str) -> str:
    if rel in {"scripts/run_flow.sh", "scripts/submit_flow.sh"}:
        return "flow_orchestrator"
    m = re.match(r"scripts/stages/([^/]+)/run\.sh$", rel)
    if m:
        return "flow_stage"
    m = re.match(r"scripts/stages/([^/]+)/run\.tcl$", rel)
    if m:
        return "flow_stage_tcl"
    if rel.startswith("scripts/stages/"):
        return "flow_stage_aux"
    if rel.startswith("scripts/tech/"):
        return "tech_utility"
    if rel.startswith("scripts/common/"):
        return "common_utility"
    if rel.startswith("scripts/debug/"):
        return "debug_tool"
    return "script"


def detect_domain(rel: str) -> str:
    if "backside" in rel or "bspdn" in rel or "gt3" in rel:
        return "backside_routing"
    if "cts" in rel or "clock" in rel:
        return "cts"
    if "route" in rel:
        return "route"
    if "place" in rel or "replace" in rel:
        return "placement"
    if rel.startswith("scripts/common/"):
        return "infrastructure"
    return "general"


def detect_stage(rel: str) -> str:
    if "preflight" in rel:
        return "preflight"
    if "place" in rel or "replace" in rel:
        return "place"
    if "cts" in rel or "clock" in rel:
        return "cts"
    if "route" in rel:
        return "route"
    if "monitor" in rel or "collect" in rel or "analyze" in rel:
        return "analysis"
    return "utility"


def detect_lang(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".sh": "bash",
        ".py": "python",
        ".tcl": "tcl",
        ".md": "markdown",
        ".yaml": "yaml",
        ".yml": "yaml",
    }.get(ext, "text")


def command_hint(rel: str) -> str:
    if rel.endswith(".sh"):
        return f"bash {rel}"
    if rel.endswith(".py"):
        return f"python3 {rel}"
    if rel.endswith(".tcl"):
        return f"# sourced by flow: {rel}"
    return ""


def summary_from_filename(path: Path) -> str:
    base = path.stem.replace("_", " ").replace("-", " ").strip()
    return base if base else "no summary"


def extract_summary(path: Path) -> str:
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        return summary_from_filename(path)

    if path.suffix == ".py":
        m = re.search(r'^\s*"""(.*?)"""', text, flags=re.S)
        if m:
            line = m.group(1).strip().splitlines()[0].strip()
            if line:
                return line

    lines = text.splitlines()[:40]
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#!"):
            continue
        if line.startswith("#"):
            line = re.sub(r"^#+\s*", "", line).strip()
            if line:
                return line
        if path.suffix == ".md" and line.startswith("#"):
            line = re.sub(r"^#+\s*", "", line).strip()
            if line:
                return line
    return summary_from_filename(path)


def make_tags(rel: str) -> str:
    toks = re.split(r"[/_\-.]+", rel.lower())
    toks = [t for t in toks if t and t not in {"scripts", "run", "sh", "py", "tcl"}]
    seen: Set[str] = set()
    uniq = []
    for t in toks:
        if t in seen:
            continue
        seen.add(t)
        uniq.append(t)
    return ",".join(uniq[:24])


def iter_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        yield p


def load_metadata(tsv_path: Path) -> Dict[str, Dict[str, str]]:
    meta: Dict[str, Dict[str, str]] = {}
    if not tsv_path.exists():
        return meta
    with tsv_path.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rel = (row.get("path") or "").strip()
            if not rel:
                continue
            meta[rel] = {k: (v or "").strip() for k, v in row.items()}
    return meta


def default_tool_id(rel: str) -> str:
    return slugify(rel.replace("scripts/", ""))


def merge_field(meta_row: Dict[str, str], key: str, fallback: str) -> str:
    val = (meta_row.get(key) or "").strip()
    return val if val else fallback


def build_catalog() -> List[Entry]:
    metadata = load_metadata(META_TSV)
    entries: List[Entry] = []
    for p in iter_files(SCRIPTS_DIR):
        rel = p.relative_to(ROOT).as_posix()
        meta = metadata.get(rel, {})

        etype = merge_field(meta, "type", detect_type(rel))
        domain = merge_field(meta, "domain", detect_domain(rel))
        stage = merge_field(meta, "stage", detect_stage(rel))
        lang = detect_lang(p)
        exec_flag = 1 if os.access(p, os.X_OK) else 0
        summary = merge_field(meta, "summary", extract_summary(p))
        tags = merge_field(meta, "tags", make_tags(rel))
        hint = merge_field(meta, "command_hint", command_hint(rel))

        entries.append(
            Entry(
                tool_id=merge_field(meta, "tool_id", default_tool_id(rel)),
                tool_type=etype,
                lifecycle=merge_field(meta, "lifecycle", "active"),
                version=merge_field(meta, "version", "0.1.0"),
                owner=merge_field(meta, "owner", "unassigned"),
                domain=domain,
                stage=stage,
                path=rel,
                lang=lang,
                executable=exec_flag,
                summary=summary,
                tags=tags,
                input_contract=merge_field(meta, "input_contract", ""),
                output_contract=merge_field(meta, "output_contract", ""),
                validator=merge_field(meta, "validator", ""),
                last_verified=merge_field(meta, "last_verified", ""),
                evidence_path=merge_field(meta, "evidence_path", ""),
                replacement_tool_id=merge_field(meta, "replacement_tool_id", ""),
                command_hint=hint,
            )
        )

    entries.sort(key=lambda e: (e.tool_type, e.path))
    return entries


def write_tsv(entries: List[Entry]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(CATALOG_FIELDS)
        for e in entries:
            w.writerow(
                [
                    e.tool_id,
                    e.tool_type,
                    e.lifecycle,
                    e.version,
                    e.owner,
                    e.domain,
                    e.stage,
                    e.path,
                    e.lang,
                    e.executable,
                    e.summary,
                    e.tags,
                    e.input_contract,
                    e.output_contract,
                    e.validator,
                    e.last_verified,
                    e.evidence_path,
                    e.replacement_tool_id,
                    e.command_hint,
                ]
            )


def write_md(entries: List[Entry]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    grouped: Dict[str, List[Entry]] = {}
    for e in entries:
        grouped.setdefault(e.tool_type, []).append(e)

    lines = []
    lines.append("# Tool / Flow Script Catalog")
    lines.append("")
    lines.append("Auto-generated from `scripts/` by `scripts/common/tool_catalog.py`.")
    lines.append("")
    lines.append("## Quick usage")
    lines.append("- Rebuild: `python3 scripts/common/tool_catalog.py build`")
    lines.append("- Query: `python3 scripts/common/tool_catalog.py query cts route`")
    lines.append("- Query with facets: `python3 scripts/common/tool_catalog.py query monitor --stage analysis --lifecycle active`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| type | count |")
    lines.append("|---|---:|")
    for t in sorted(grouped):
        lines.append(f"| {t} | {len(grouped[t])} |")
    lines.append("")

    for t in sorted(grouped):
        lines.append(f"## {t}")
        lines.append("")
        lines.append("| tool_id | lifecycle | version | stage | path | summary |")
        lines.append("|---|---|---|---|---|---|")
        for e in grouped[t]:
            summary = e.summary.replace("|", "/")
            lines.append(
                f"| `{e.tool_id}` | {e.lifecycle} | {e.version} | {e.stage} | `{e.path}` | {summary} |"
            )
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n")


def load_entries(tsv_path: Path) -> List[Entry]:
    out: List[Entry] = []
    with tsv_path.open() as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            out.append(
                Entry(
                    tool_id=row.get("tool_id", ""),
                    tool_type=row.get("type", ""),
                    lifecycle=row.get("lifecycle", "active"),
                    version=row.get("version", "0.1.0"),
                    owner=row.get("owner", "unassigned"),
                    domain=row.get("domain", "general"),
                    stage=row.get("stage", "utility"),
                    path=row.get("path", ""),
                    lang=row.get("lang", "text"),
                    executable=int(row.get("executable", "0") or 0),
                    summary=row.get("summary", ""),
                    tags=row.get("tags", ""),
                    input_contract=row.get("input_contract", ""),
                    output_contract=row.get("output_contract", ""),
                    validator=row.get("validator", ""),
                    last_verified=row.get("last_verified", ""),
                    evidence_path=row.get("evidence_path", ""),
                    replacement_tool_id=row.get("replacement_tool_id", ""),
                    command_hint=row.get("command_hint", ""),
                )
            )
    return out


def score_entry(e: Entry, terms: List[str]) -> float:
    hay_path = e.path.lower()
    hay_summary = e.summary.lower()
    hay_tags = e.tags.lower()
    hay_misc = " ".join([
        e.tool_id,
        e.domain,
        e.stage,
        e.owner,
        e.command_hint,
        e.input_contract,
        e.output_contract,
    ]).lower()
    score = 0.0
    for t in terms:
        if t in hay_path:
            score += 2.0
        if t in hay_summary:
            score += 1.8
        if t in hay_tags:
            score += 1.4
        if t in hay_misc:
            score += 1.0
    return score


def query_entries(
    entries: List[Entry],
    terms: List[str],
    typ: Optional[str],
    lifecycle: Optional[str],
    stage: Optional[str],
    domain: Optional[str],
    owner: Optional[str],
    lang: Optional[str],
) -> List[Entry]:
    terms_l = [t.lower() for t in terms]
    scored = []
    for e in entries:
        if typ and e.tool_type != typ:
            continue
        if lifecycle and e.lifecycle != lifecycle:
            continue
        if stage and e.stage != stage:
            continue
        if domain and e.domain != domain:
            continue
        if owner and e.owner != owner:
            continue
        if lang and e.lang != lang:
            continue
        s = score_entry(e, terms_l)
        if s <= 0:
            continue
        scored.append((s, e))
    scored.sort(key=lambda x: (-x[0], x[1].path))
    return [x[1] for x in scored]


def cmd_build(_: argparse.Namespace) -> int:
    entries = build_catalog()
    write_tsv(entries)
    write_md(entries)
    print(f"generated: {OUT_TSV}")
    print(f"generated: {OUT_MD}")
    print(f"entries: {len(entries)}")
    if META_TSV.exists():
        print(f"metadata: {META_TSV}")
    else:
        print(f"metadata: {META_TSV} (optional; missing)")
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    if not OUT_TSV.exists():
        print("catalog missing; run build first")
        return 2
    entries = load_entries(OUT_TSV)
    hits = query_entries(
        entries,
        args.terms,
        args.type,
        args.lifecycle,
        args.stage,
        args.domain,
        args.owner,
        args.lang,
    )
    if args.limit:
        hits = hits[: args.limit]
    if not hits:
        print("no match")
        return 1
    print("| tool_id | type | lifecycle | version | stage | owner | path | summary | hint |")
    print("|---|---|---|---|---|---|---|---|---|")
    for e in hits:
        summary = e.summary.replace("|", "/")
        hint = e.command_hint.replace("|", "/")
        print(
            f"| {e.tool_id} | {e.tool_type} | {e.lifecycle} | {e.version} | {e.stage} | {e.owner} | `{e.path}` | {summary} | `{hint}` |"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Tool/flow catalog builder and query tool")
    sub = p.add_subparsers(dest="cmd")
    sub.required = True

    p_build = sub.add_parser("build", help="scan scripts and generate catalog files")
    p_build.set_defaults(func=cmd_build)

    p_query = sub.add_parser("query", help="query generated catalog")
    p_query.add_argument("terms", nargs="+", help="search terms")
    p_query.add_argument("--type", default=None, help="filter by type")
    p_query.add_argument("--lifecycle", default=None, help="filter by lifecycle")
    p_query.add_argument("--stage", default=None, help="filter by stage")
    p_query.add_argument("--domain", default=None, help="filter by domain")
    p_query.add_argument("--owner", default=None, help="filter by owner")
    p_query.add_argument("--lang", default=None, help="filter by language")
    p_query.add_argument("--limit", type=int, default=50, help="max rows")
    p_query.set_defaults(func=cmd_query)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
