#!/usr/bin/env python3
"""Build paired ours-vs-vanilla deltas from route manifests.

This script is intentionally conservative: it only emits paired rows when
both modes exist for the same design in one manifest.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List


PAIR_KEYS = ("Power(mW)", "WNS(ns)", "TNS(ns)", "HPWL(um)", "Area(um^2)")


def as_float(v: str) -> float:
    try:
        return float(v)
    except Exception:
        return float("nan")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", action="append", required=True, help="run manifest TSV path; can be repeated")
    ap.add_argument("--out-tsv", required=True)
    return ap.parse_args()


def load_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def mode_from_row(r: Dict[str, str]) -> str:
    mode = (r.get("mode") or "").strip()
    if mode:
        return mode
    # fallback for some monitor-expanded rows
    return (r.get("label") or "").strip()


def metric_from_row(r: Dict[str, str], key: str) -> str:
    # Allow both manifest-native and monitor-backfilled names.
    if key in r and r[key] not in ("", None):
        return str(r[key])
    alt = {
        "Power(mW)": "power_mw",
        "WNS(ns)": "wns_ns",
        "TNS(ns)": "tns_ns",
        "HPWL(um)": "hpwl_um",
        "Area(um^2)": "area_um2",
    }.get(key, "")
    return str(r.get(alt, "")) if alt else ""


def build_pairs(manifest_path: Path, rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    by_design: Dict[str, Dict[str, Dict[str, str]]] = {}
    for r in rows:
        design = (r.get("design") or "").strip()
        mode = mode_from_row(r)
        if not design or mode not in ("vanilla_replace", "ours_replace"):
            continue
        by_design.setdefault(design, {})[mode] = r

    out: List[Dict[str, str]] = []
    for design, mm in sorted(by_design.items()):
        if "vanilla_replace" not in mm or "ours_replace" not in mm:
            continue
        base = mm["vanilla_replace"]
        ours = mm["ours_replace"]
        row: Dict[str, str] = {
            "manifest": str(manifest_path),
            "design": design,
            "vanilla_job": str(base.get("job_id", "")),
            "ours_job": str(ours.get("job_id", "")),
            "vanilla_status": str(base.get("status", "")),
            "ours_status": str(ours.get("status", "")),
            "vanilla_result": str(base.get("result", "")),
            "ours_result": str(ours.get("result", "")),
        }
        for k in PAIR_KEYS:
            v0 = metric_from_row(base, k)
            v1 = metric_from_row(ours, k)
            row[f"vanilla_{k}"] = v0
            row[f"ours_{k}"] = v1
            f0 = as_float(v0)
            f1 = as_float(v1)
            row[f"delta_{k}_ours_minus_vanilla"] = "" if (f0 != f0 or f1 != f1) else f"{(f1 - f0):.6f}"
        out.append(row)
    return out


def main() -> int:
    args = parse_args()
    out_path = Path(args.out_tsv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows_all: List[Dict[str, str]] = []
    for m in args.manifest:
        p = Path(m)
        if not p.is_file():
            continue
        rows_all.extend(build_pairs(p, load_rows(p)))

    fields = [
        "manifest",
        "design",
        "vanilla_job",
        "ours_job",
        "vanilla_status",
        "ours_status",
        "vanilla_result",
        "ours_result",
    ]
    for k in PAIR_KEYS:
        fields.extend([f"vanilla_{k}", f"ours_{k}", f"delta_{k}_ours_minus_vanilla"])

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        for r in rows_all:
            w.writerow(r)

    print(f"wrote: {out_path}")
    print(f"pairs: {len(rows_all)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
