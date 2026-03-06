#!/usr/bin/env python3
"""Unified PDK/flow preflight checks before route submissions."""

import argparse
import pathlib
import re
import sys
from typing import Dict, List, Optional, Set


TECH_LAYER_RE = re.compile(r"^\s*LAYER\s+(\S+)")
LEF_REF_LAYER_RE = re.compile(r"\bLAYER\s+([^\s;]+)")
DEF_TRACK_LAYER_RE = re.compile(r"^\s*TRACKS\s+.*\bLAYER\s+([^\s;]+)")


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_tech_layers(techlef: pathlib.Path) -> Set[str]:
    out: Set[str] = set()
    for ln in read_text(techlef).splitlines():
        m = TECH_LAYER_RE.match(ln)
        if m:
            out.add(m.group(1))
    return out


def parse_lef_refs(lef_files: List[pathlib.Path]) -> Set[str]:
    out: Set[str] = set()
    for lf in lef_files:
        txt = read_text(lf)
        for m in LEF_REF_LAYER_RE.finditer(txt):
            out.add(m.group(1))
    return out


def parse_def_track_layers(def_file: Optional[pathlib.Path]) -> Set[str]:
    if def_file is None or (not def_file.is_file()):
        return set()
    out: Set[str] = set()
    for ln in read_text(def_file).splitlines():
        m = DEF_TRACK_LAYER_RE.match(ln)
        if m:
            out.add(m.group(1))
    return out


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


def write_report(
    out_md: pathlib.Path,
    checks: List[Dict[str, str]],
    summary: Dict[str, str],
    suggestions: List[str],
) -> None:
    lines = [
        "# PDK/Flow Unified Preflight",
        "",
        "- verdict: `{}`".format(summary["verdict"]),
        "- fail_count: `{}`".format(summary["fail_count"]),
        "- warn_count: `{}`".format(summary["warn_count"]),
        "",
        "| check | level | status | detail |",
        "|---|---|---|---|",
    ]
    for c in checks:
        lines.append(
            "| {} | {} | {} | {} |".format(
                c["check"],
                c["level"],
                c["status"],
                c["detail"],
            )
        )
    if suggestions:
        lines += ["", "## Suggestions", ""]
        for s in suggestions:
            lines.append("- {}".format(s))
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Unified PDK/flow preflight checker")
    ap.add_argument("--techlef", required=True)
    ap.add_argument("--lef-dir", required=True)
    ap.add_argument("--lib-dir", default="")
    ap.add_argument("--netlist", required=True)
    ap.add_argument("--sdc", required=True)
    ap.add_argument("--resume-def", default="")
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--ignore-layer", action="append", default=["OVERLAP"])
    args = ap.parse_args()

    techlef = pathlib.Path(args.techlef).resolve()
    lef_dir = pathlib.Path(args.lef_dir).resolve()
    lib_dir = pathlib.Path(args.lib_dir).resolve() if args.lib_dir else None
    netlist = pathlib.Path(args.netlist).resolve()
    sdc = pathlib.Path(args.sdc).resolve()
    resume_def = pathlib.Path(args.resume_def).resolve() if args.resume_def else None
    out_md = pathlib.Path(args.out_md).resolve()
    out_md.parent.mkdir(parents=True, exist_ok=True)

    checks: List[Dict[str, str]] = []
    suggestions: List[str] = []

    def add(check: str, level: str, ok: bool, detail: str) -> None:
        checks.append(
            {
                "check": check,
                "level": level,
                "status": "PASS" if ok else ("WARN" if level == "warn" else "FAIL"),
                "detail": detail.replace("|", "/"),
            }
        )

    add("techlef_exists", "hard", techlef.is_file(), str(techlef))
    add("lef_dir_exists", "hard", lef_dir.is_dir(), str(lef_dir))
    add("netlist_exists", "hard", netlist.is_file(), str(netlist))
    add("sdc_exists", "hard", sdc.is_file(), str(sdc))
    if resume_def is not None:
        add("resume_def_exists", "hard", resume_def.is_file(), str(resume_def))
    if lib_dir is not None:
        add("lib_dir_exists", "hard", lib_dir.is_dir(), str(lib_dir))
        if lib_dir.is_dir():
            nlib = len(list(lib_dir.glob("*.lib")))
            add("lib_count", "warn", nlib > 0, "lib_count={}".format(nlib))

    if techlef.is_file() and lef_dir.is_dir():
        lef_files = sorted(lef_dir.glob("*.lef"))
        add("lef_count", "hard", len(lef_files) > 0, "lef_count={}".format(len(lef_files)))
        if lef_files:
            tech_layers = parse_tech_layers(techlef)
            lef_refs = parse_lef_refs(lef_files)
            def_refs = parse_def_track_layers(resume_def)
            ignore = set(args.ignore_layer or [])
            refs = (lef_refs | def_refs) - ignore
            missing = sorted(x for x in refs if x not in tech_layers)

            t_style = style_hint(tech_layers)
            l_style = style_hint(lef_refs)
            d_style = style_hint(def_refs)
            add("layer_style", "warn", True, "tech={} lef={} def={}".format(t_style, l_style, d_style))
            if len(missing) == 0:
                add("layer_compat", "hard", True, "missing=0")
            else:
                add("layer_compat", "hard", False, "missing={} first={}".format(len(missing), ",".join(missing[:8])))
                if t_style == "M/V" and l_style == "metal/via":
                    suggestions.append(
                        "Detected namespace mismatch (tech: M/V vs design: metal/via). Do not resubmit before layer-map compatibility is fixed."
                    )
                else:
                    suggestions.append(
                        "Fix missing layer definitions in tech LEF or adjust design LEF/DEF layer naming to match tech stack."
                    )

    fail_count = sum(1 for c in checks if c["status"] == "FAIL")
    warn_count = sum(1 for c in checks if c["status"] == "WARN")
    verdict = "PASS" if fail_count == 0 else "FAIL"
    summary = {
        "verdict": verdict,
        "fail_count": str(fail_count),
        "warn_count": str(warn_count),
    }
    write_report(out_md, checks, summary, suggestions)

    print("out_md={}".format(out_md))
    print("verdict={}".format(verdict))
    print("fail_count={}".format(fail_count))
    print("warn_count={}".format(warn_count))
    return 0 if fail_count == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
