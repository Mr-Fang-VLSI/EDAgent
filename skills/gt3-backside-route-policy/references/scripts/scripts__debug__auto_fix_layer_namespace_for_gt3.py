#!/usr/bin/env python3
"""Auto-fix ChiPBench-style layer namespace to GT3-style names.

Transforms design LEF/DEF text in a copied workspace:
- metalN -> MN
- viaN   -> VN
- poly   -> GATE
- active -> ACT
- nwell  -> NW
- contact -> CONT

Designed for preflight remediation before GT3 Innovus submission.
"""

import argparse
import pathlib
import re
import shutil
from typing import Dict, List, Tuple


TOKEN_MAP: Dict[str, str] = {
    "poly": "GATE",
    "active": "ACT",
    "nwell": "NW",
    "contact": "CONT",
}


def build_pattern_replacements(include_token_map: bool = True) -> List[Tuple[object, str]]:
    reps: List[Tuple[object, str]] = []
    # High indices first to avoid partial replacements (e.g. metal1 in metal10).
    for i in range(20, 0, -1):
        reps.append((re.compile(r"\bmetal{}\b".format(i), flags=re.IGNORECASE), "M{}".format(i)))
    for i in range(20, 0, -1):
        reps.append((re.compile(r"\bvia{}\b".format(i), flags=re.IGNORECASE), "V{}".format(i)))
    if include_token_map:
        for src, dst in TOKEN_MAP.items():
            reps.append((re.compile(r"\b{}\b".format(re.escape(src)), flags=re.IGNORECASE), dst))
    return reps


def transform_text(text: str, reps: List[Tuple[object, str]]) -> Tuple[str, int]:
    out = text
    total = 0
    for pat, dst in reps:
        out, n = pat.subn(dst, out)
        total += n
    return out, total


def extract_site_blocks(text: str) -> List[str]:
    lines = text.splitlines()
    out: List[str] = []
    i = 0
    n = len(lines)
    while i < n:
        m = re.match(r"^\s*SITE\s+(\S+)", lines[i], flags=re.IGNORECASE)
        if not m:
            i += 1
            continue
        site_name = m.group(1)
        block = [lines[i]]
        i += 1
        while i < n:
            block.append(lines[i])
            if re.match(r"^\s*END\s+{}\s*$".format(re.escape(site_name)), lines[i], flags=re.IGNORECASE):
                break
            i += 1
        out.append("\n".join(block))
        i += 1
    return out


def write_report(
    out_md: pathlib.Path,
    src_lef_dir: pathlib.Path,
    src_def: pathlib.Path,
    out_lef_dir: pathlib.Path,
    out_def: pathlib.Path,
    file_counts: List[Tuple[str, int]],
    dropped_files: List[str],
    site_block_count: int,
    site_file: pathlib.Path,
) -> None:
    total_repl = sum(n for _, n in file_counts)
    lines: List[str] = []
    lines.append("# GT3 Namespace Auto-Fix Report")
    lines.append("")
    lines.append("- src_lef_dir: `{}`".format(src_lef_dir))
    lines.append("- src_resume_def: `{}`".format(src_def))
    lines.append("- out_lef_dir: `{}`".format(out_lef_dir))
    lines.append("- out_resume_def: `{}`".format(out_def))
    lines.append("- total_replacements: `{}`".format(total_repl))
    lines.append("")
    if dropped_files:
        lines.append("## Dropped LEFs")
        lines.append("")
        for p in dropped_files:
            lines.append("- `{}`".format(p))
        lines.append("")
    lines.append("## Preserved SITE blocks")
    lines.append("")
    lines.append("- count: `{}`".format(site_block_count))
    if site_block_count > 0:
        lines.append("- file: `{}`".format(site_file))
    lines.append("")
    lines.append("## Per-file replacements")
    lines.append("")
    lines.append("| file | replacements |")
    lines.append("|---|---:|")
    for p, n in file_counts:
        lines.append("| {} | {} |".format(p, n))
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Auto-fix LEF/DEF layer namespace for GT3")
    ap.add_argument("--lef-dir", required=True)
    ap.add_argument("--resume-def", required=True)
    ap.add_argument("--out-lef-dir", required=True)
    ap.add_argument("--out-def", required=True)
    ap.add_argument("--report-md", required=True)
    ap.add_argument("--drop-techlef", type=int, default=1, help="Drop *.tech.lef from copied LEF dir")
    args = ap.parse_args()

    lef_dir = pathlib.Path(args.lef_dir).resolve()
    resume_def = pathlib.Path(args.resume_def).resolve()
    out_lef_dir = pathlib.Path(args.out_lef_dir).resolve()
    out_def = pathlib.Path(args.out_def).resolve()
    report_md = pathlib.Path(args.report_md).resolve()

    if not lef_dir.is_dir():
        raise SystemExit("ERROR: lef-dir not found: {}".format(lef_dir))
    if not resume_def.is_file():
        raise SystemExit("ERROR: resume-def not found: {}".format(resume_def))

    if out_lef_dir.exists():
        shutil.rmtree(str(out_lef_dir))
    out_lef_dir.mkdir(parents=True, exist_ok=True)
    out_def.parent.mkdir(parents=True, exist_ok=True)
    report_md.parent.mkdir(parents=True, exist_ok=True)

    # LEF: full mapping is acceptable because layer keywords are dominant.
    # DEF: keep only metal/via token mapping to avoid corrupting instance/net names
    # such as "*.active$_SDFFE_*" in ChiPBench netlists/DEFs.
    reps_lef = build_pattern_replacements(include_token_map=True)
    reps_def = build_pattern_replacements(include_token_map=False)

    dropped: List[str] = []
    per_file: List[Tuple[str, int]] = []
    site_blocks: List[str] = []

    lef_files = sorted(lef_dir.glob("*.lef"))
    if not lef_files:
        raise SystemExit("ERROR: no LEF files under {}".format(lef_dir))

    for src in lef_files:
        name = src.name
        if int(args.drop_techlef) == 1 and name.lower().endswith(".tech.lef"):
            dropped.append(name)
            tech_txt = src.read_text(encoding="utf-8", errors="ignore")
            site_blocks.extend(extract_site_blocks(tech_txt))
            continue
        txt = src.read_text(encoding="utf-8", errors="ignore")
        new_txt, cnt = transform_text(txt, reps_lef)
        dst = out_lef_dir / name
        dst.write_text(new_txt, encoding="utf-8")
        per_file.append((name, cnt))

    def_txt = resume_def.read_text(encoding="utf-8", errors="ignore")
    def_new, def_cnt = transform_text(def_txt, reps_def)
    out_def.write_text(def_new, encoding="utf-8")
    per_file.append((out_def.name, def_cnt))

    site_file = out_lef_dir / "chipbench_site_defs.lef"
    if site_blocks:
        site_payload = []
        site_payload.append("VERSION 5.8 ;")
        site_payload.append("BUSBITCHARS \"[]\" ;")
        site_payload.append("DIVIDERCHAR \"/\" ;")
        site_payload.append("")
        for b in site_blocks:
            site_payload.append(b)
            site_payload.append("")
        site_payload.append("END LIBRARY")
        site_file.write_text("\n".join(site_payload) + "\n", encoding="utf-8")
        per_file.append((site_file.name, 0))

    write_report(
        out_md=report_md,
        src_lef_dir=lef_dir,
        src_def=resume_def,
        out_lef_dir=out_lef_dir,
        out_def=out_def,
        file_counts=per_file,
        dropped_files=dropped,
        site_block_count=len(site_blocks),
        site_file=site_file,
    )

    print("out_lef_dir={}".format(out_lef_dir))
    print("out_def={}".format(out_def))
    print("report_md={}".format(report_md))
    print("total_replacements={}".format(sum(x[1] for x in per_file)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
