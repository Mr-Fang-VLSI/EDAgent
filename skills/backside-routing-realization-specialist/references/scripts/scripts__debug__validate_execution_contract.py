#!/usr/bin/env python3
"""Validate execution contract for flow manifests.

This script enforces a stronger definition of "SUCCESS":
1) no fatal signatures in logs,
2) required route artifacts exist for route-phase runs,
3) key QoR metrics are not NA (configurable strictness),
4) precheck failures are explicitly surfaced.
"""

import argparse
import csv
import pathlib
import re
import sys
from typing import Dict, List, Optional, Tuple


DEFAULT_FATAL_PATTERNS = [
    r"IMPSYT-16013",
    r"IMPSYT-6692",
    r"IMPLF-3\)",
    r"IMPLF-53\)",
    r"IMPLF-111\)",
    r"IMPLF-224\)",
    r"ERROR:\s+routeDesign failed",
    r"ERROR:\s+cannot proceed to 'route'",
    r"\*\*ERROR:\s+\(IMPVL-209\)",
    r"\*\*ERROR:\s+\(IMPDF-138\)",
    r"NRGR-6\).*Cannot do global route",
    r"fatal Innovus signatures detected",
]


def is_na(v: str) -> bool:
    s = (v or "").strip().upper()
    return s in {"", "NA", "N/A", "NONE", "-"}


def parse_design_from_run_dir(run_dir: str) -> str:
    p = pathlib.Path(run_dir)
    parts = p.parts
    for i, tok in enumerate(parts):
        if tok == "outputs" and i + 1 < len(parts):
            return parts[i + 1]
    return "NA"


def parse_run_dir_from_out_log(out_log: pathlib.Path) -> str:
    if not out_log.is_file():
        return "NA"
    pat = re.compile(r'set OUT_DIR "([^"]+)"')
    try:
        with out_log.open("r", encoding="utf-8", errors="ignore") as f:
            for ln in f:
                m = pat.search(ln)
                if m:
                    return m.group(1)
    except OSError:
        return "NA"
    return "NA"


def read_tail(path: pathlib.Path, max_bytes: int = 1024 * 1024) -> str:
    if not path.is_file():
        return ""
    try:
        with path.open("rb") as f:
            f.seek(0, 2)
            size = f.tell()
            start = max(0, size - max_bytes)
            f.seek(start)
            blob = f.read().decode("utf-8", errors="ignore")
        if start > 0 and "\n" in blob:
            blob = blob.split("\n", 1)[1]
        return blob
    except OSError:
        return ""


def find_fatal(paths: List[pathlib.Path], patterns: List[object]) -> Optional[Tuple[str, str]]:
    for p in paths:
        txt = read_tail(p)
        if not txt:
            continue
        for rgx in patterns:
            m = rgx.search(txt)
            if m:
                return str(p), rgx.pattern
    return None


def phase_of_row(row: Dict[str, str]) -> str:
    phase = (row.get("phase") or "").strip().lower()
    if phase:
        if phase == "prep":
            return "placement"
        return phase
    mode = (row.get("mode") or "").strip().lower()
    if "route" in mode:
        return "route"
    if "place" in mode or mode.startswith("prep"):
        return "placement"
    return "other"


def build_route_artifact_paths(run_dir: pathlib.Path, design: str) -> List[pathlib.Path]:
    reports = run_dir / "reports"
    cands = [
        reports / (design + "_postRoute.summary.gz"),
        reports / (design + "_postroute.summary.gz"),
        reports / "area_postroute.rpt",
        reports / "area_postRoute.rpt",
        reports / "power_postroute.rpt",
        reports / "power_postRoute.rpt",
        reports / "timing_postroute.rpt",
        run_dir / (design + ".routed.def"),
    ]
    return cands


def validate_row(
    row: Dict[str, str],
    root: pathlib.Path,
    fatal_patterns: List[object],
    require_route_metrics: bool,
) -> Dict[str, str]:
    verdict = "PASS"
    reasons: List[str] = []

    status = (row.get("status") or "").strip().upper()
    result = (row.get("result") or "").strip().upper()

    run_dir_s = (row.get("run_dir") or "").strip()
    if is_na(run_dir_s):
        out_s = (row.get("stdout") or "").strip()
        if out_s and not is_na(out_s):
            guessed = parse_run_dir_from_out_log(pathlib.Path(out_s))
            if guessed != "NA":
                run_dir_s = guessed

    run_dir = pathlib.Path(run_dir_s) if run_dir_s and not is_na(run_dir_s) else None
    if run_dir and not run_dir.is_absolute():
        run_dir = (root / run_dir).resolve()

    design = (row.get("design") or "").strip()
    if is_na(design) and run_dir is not None:
        design = parse_design_from_run_dir(str(run_dir))
    if is_na(design):
        design = "NA"

    phase = phase_of_row(row)

    if status in {"PRECHECK_FAIL", "FAIL", "FAILED"} or result == "FAIL":
        verdict = "FAIL"
        reasons.append("manifest_status_fail")

    logs: List[pathlib.Path] = []
    for k in ("stdout", "stderr"):
        p = (row.get(k) or "").strip()
        if p and not is_na(p):
            pp = pathlib.Path(p)
            if not pp.is_absolute():
                pp = (root / pp).resolve()
            logs.append(pp)
    if run_dir is not None and design != "NA":
        logs.append(root / "logs" / design / "innovus" / run_dir.name / "innovus.log")

    fatal_hit = find_fatal(logs, fatal_patterns)
    if fatal_hit is not None:
        verdict = "FAIL"
        reasons.append("fatal_log:" + fatal_hit[1])

    if run_dir is None:
        verdict = "FAIL"
        reasons.append("missing_run_dir")
    else:
        status_file = run_dir / "status.txt"
        if status_file.is_file():
            try:
                st = status_file.read_text(encoding="utf-8", errors="ignore").strip().upper()
            except OSError:
                st = ""
            if st and st != "SUCCESS":
                verdict = "FAIL"
                reasons.append("status_txt_not_success:" + st)

    if phase == "route" and run_dir is not None and design != "NA":
        route_artifacts = build_route_artifact_paths(run_dir, design)
        if not any(p.is_file() for p in route_artifacts):
            verdict = "FAIL"
            reasons.append("missing_route_artifacts")

        if require_route_metrics:
            for key in ("hpwl_um", "area_um2", "power_mw", "wns_ns", "tns_ns"):
                if key in row and is_na(row.get(key, "")):
                    verdict = "FAIL"
                    reasons.append("na_metric:" + key)

    if phase == "placement":
        hpwl = row.get("hpwl_um", "")
        if "hpwl_um" in row and is_na(hpwl):
            # Placement-only rows may not fill every metric, but HPWL should exist when available.
            reasons.append("warn_na_hpwl")

    if not reasons:
        reasons.append("ok")

    return {
        "design": design,
        "phase": phase,
        "mode": (row.get("mode") or "NA").strip(),
        "job_id": (row.get("job_id") or "NA").strip(),
        "status": status or "NA",
        "result": result or "NA",
        "verdict": verdict,
        "reasons": ";".join(reasons),
        "run_dir": str(run_dir) if run_dir is not None else "NA",
        "stdout": (row.get("stdout") or "NA").strip() or "NA",
    }


def render_md(
    out_md: pathlib.Path,
    manifest: pathlib.Path,
    rows: List[Dict[str, str]],
) -> None:
    total = len(rows)
    fail = sum(1 for r in rows if r["verdict"] == "FAIL")
    passed = total - fail
    lines = [
        "# Execution Contract Validation",
        "",
        "- manifest: `{}`".format(manifest),
        "- total_rows: `{}`".format(total),
        "- pass_rows: `{}`".format(passed),
        "- fail_rows: `{}`".format(fail),
        "",
        "| design | phase | mode | job_id | status | result | verdict | reasons |",
        "|---|---|---|---:|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                r["design"],
                r["phase"],
                r["mode"],
                r["job_id"],
                r["status"],
                r["result"],
                r["verdict"],
                r["reasons"],
            )
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Validate execution contract against manifest rows")
    ap.add_argument("--manifest", required=True, help="Input manifest TSV")
    ap.add_argument("--root", default=".", help="Project root for relative paths")
    ap.add_argument("--out-prefix", required=True, help="Output prefix for .tsv/.md")
    ap.add_argument("--fatal-pattern", action="append", default=[], help="Extra fatal regex patterns")
    ap.add_argument("--require-route-metrics", type=int, default=1, help="1: fail route rows with NA key metrics")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    manifest = pathlib.Path(args.manifest).resolve()
    root = pathlib.Path(args.root).resolve()
    out_prefix = pathlib.Path(args.out_prefix).resolve()

    if not manifest.is_file():
        print("ERROR: manifest not found: {}".format(manifest), file=sys.stderr)
        return 2

    fatal_src = DEFAULT_FATAL_PATTERNS + list(args.fatal_pattern or [])
    fatal_patterns = [re.compile(p) for p in fatal_src]

    with manifest.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        rd = csv.DictReader(f, delimiter="\t")
        rows_in = list(rd)

    rows_out: List[Dict[str, str]] = []
    for row in rows_in:
        rows_out.append(
            validate_row(
                row=row,
                root=root,
                fatal_patterns=fatal_patterns,
                require_route_metrics=bool(args.require_route_metrics),
            )
        )

    out_tsv = pathlib.Path(str(out_prefix) + ".tsv")
    out_md = pathlib.Path(str(out_prefix) + ".md")
    out_tsv.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "design",
        "phase",
        "mode",
        "job_id",
        "status",
        "result",
        "verdict",
        "reasons",
        "run_dir",
        "stdout",
    ]
    with out_tsv.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        wr.writeheader()
        for r in rows_out:
            wr.writerow(r)

    render_md(out_md, manifest, rows_out)

    fail = sum(1 for r in rows_out if r["verdict"] == "FAIL")
    print("manifest={}".format(manifest))
    print("rows={}".format(len(rows_out)))
    print("fail_rows={}".format(fail))
    print("out_tsv={}".format(out_tsv))
    print("out_md={}".format(out_md))
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
