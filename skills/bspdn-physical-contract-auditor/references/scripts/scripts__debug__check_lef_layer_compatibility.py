#!/usr/bin/env python3
"""Check technology LEF vs design LEF/DEF layer-name compatibility."""

import argparse
import pathlib
import re
import sys
from typing import Iterable, List, Optional, Set


TECH_LAYER_RE = re.compile(r"^\s*LAYER\s+(\S+)")
LEF_REF_LAYER_RE = re.compile(r"\bLAYER\s+([^\s;]+)")
DEF_TRACK_LAYER_RE = re.compile(r"^\s*TRACKS\s+.*\bLAYER\s+([^\s;]+)")


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_tech_layers(techlef: pathlib.Path) -> Set[str]:
    layers: Set[str] = set()
    for ln in read_text(techlef).splitlines():
        m = TECH_LAYER_RE.match(ln)
        if m:
            layers.add(m.group(1))
    return layers


def parse_lef_refs(lef_files: Iterable[pathlib.Path]) -> Set[str]:
    refs: Set[str] = set()
    for lf in lef_files:
        txt = read_text(lf)
        for m in LEF_REF_LAYER_RE.finditer(txt):
            refs.add(m.group(1))
    return refs


def parse_def_track_layers(def_file: Optional[pathlib.Path]) -> Set[str]:
    if def_file is None or (not def_file.is_file()):
        return set()
    refs: Set[str] = set()
    for ln in read_text(def_file).splitlines():
        m = DEF_TRACK_LAYER_RE.match(ln)
        if m:
            refs.add(m.group(1))
    return refs


def style_hint(layer_set: Set[str]) -> str:
    has_m = any(re.fullmatch(r"M\d+", x) for x in layer_set)
    has_v = any(re.fullmatch(r"V\d+", x) for x in layer_set)
    has_metal = any(re.fullmatch(r"metal\d+", x, flags=re.IGNORECASE) for x in layer_set)
    has_via = any(re.fullmatch(r"via\d+", x, flags=re.IGNORECASE) for x in layer_set)
    if has_metal or has_via:
        return "metal/via"
    if has_m or has_v:
        return "M/V"
    return "unknown"


def write_report_md(
    out_md: pathlib.Path,
    techlef: pathlib.Path,
    lef_files: List[pathlib.Path],
    def_file: Optional[pathlib.Path],
    tech_layers: Set[str],
    lef_refs: Set[str],
    def_refs: Set[str],
    missing: Set[str],
) -> None:
    lines: List[str] = []
    lines.append("# LEF/DEF Layer Compatibility Check")
    lines.append("")
    lines.append(f"- tech_lef: `{techlef}`")
    lines.append(f"- lef_count: `{len(lef_files)}`")
    lines.append(f"- def_file: `{def_file if def_file else 'NA'}`")
    lines.append(f"- tech_style: `{style_hint(tech_layers)}`")
    lines.append(f"- design_lef_style: `{style_hint(lef_refs)}`")
    lines.append(f"- def_tracks_style: `{style_hint(def_refs)}`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- tech_layers: `{len(tech_layers)}`")
    lines.append(f"- design_lef_refs: `{len(lef_refs)}`")
    lines.append(f"- def_track_refs: `{len(def_refs)}`")
    lines.append(f"- missing_refs: `{len(missing)}`")
    lines.append("")
    lines.append("## Missing Layer Names")
    lines.append("")
    if missing:
        for x in sorted(missing):
            lines.append(f"- `{x}`")
    else:
        lines.append("- none")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Check tech/design layer compatibility")
    ap.add_argument("--techlef", required=True, help="Technology LEF path")
    ap.add_argument("--lef-dir", required=True, help="Directory containing design LEF files")
    ap.add_argument("--def", dest="def_file", default="", help="Optional DEF path for TRACKS layer check")
    ap.add_argument("--ignore-layer", action="append", default=["OVERLAP"], help="Layer name to ignore (repeatable)")
    ap.add_argument("--out-md", default="", help="Optional markdown report output path")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    techlef = pathlib.Path(args.techlef).resolve()
    lef_dir = pathlib.Path(args.lef_dir).resolve()
    def_file = pathlib.Path(args.def_file).resolve() if args.def_file else None

    if not techlef.is_file():
        print(f"ERROR: tech LEF not found: {techlef}", file=sys.stderr)
        return 2
    if not lef_dir.is_dir():
        print(f"ERROR: LEF dir not found: {lef_dir}", file=sys.stderr)
        return 2

    lef_files = sorted(lef_dir.glob("*.lef"))
    if not lef_files:
        print(f"ERROR: no LEFs found under {lef_dir}", file=sys.stderr)
        return 2

    tech_layers = parse_tech_layers(techlef)
    lef_refs = parse_lef_refs(lef_files)
    def_refs = parse_def_track_layers(def_file)

    ignore = set(args.ignore_layer or [])
    refs = (lef_refs | def_refs) - ignore
    missing = {x for x in refs if x not in tech_layers}

    if args.out_md:
        out_md = pathlib.Path(args.out_md).resolve()
        out_md.parent.mkdir(parents=True, exist_ok=True)
        write_report_md(
            out_md=out_md,
            techlef=techlef,
            lef_files=lef_files,
            def_file=def_file,
            tech_layers=tech_layers,
            lef_refs=lef_refs,
            def_refs=def_refs,
            missing=missing,
        )

    print(f"tech_style={style_hint(tech_layers)} design_style={style_hint(lef_refs)} def_style={style_hint(def_refs)}")
    print(f"tech_layers={len(tech_layers)} refs={len(refs)} missing={len(missing)}")
    if missing:
        print("missing_layers=" + ",".join(sorted(missing)))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
