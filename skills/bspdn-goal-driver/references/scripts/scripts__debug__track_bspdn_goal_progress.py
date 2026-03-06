#!/usr/bin/env python3
"""Track BSPDN goal progress from a consolidated PPA markdown table."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List


@dataclass
class Row:
    mode: str
    d_hpwl_pct: float
    d_area_pct: float
    d_power_pct: float
    d_wns_ns: float
    d_tns_ns: float


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Track progress toward BSPDN goal")
    ap.add_argument(
        "--campaign-md",
        default="slurm_logs/04_delay_modeling/campaign15_route15_ppa_vs_vanilla_20260305.md",
        help="markdown file with consolidated PPA delta table",
    )
    ap.add_argument(
        "--out-prefix",
        default="slurm_logs/04_delay_modeling/bspdn_goal_progress_latest",
        help="output prefix for summary/detail artifacts",
    )
    ap.add_argument("--target-power-delta-pct", type=float, default=-8.0)
    ap.add_argument("--target-freq-improve-pct", type=float, default=5.0)
    return ap.parse_args()


def parse_pct(x: str) -> float:
    return float(x.replace("%", "").replace("+", "").strip())


def parse_num(x: str) -> float:
    return float(x.strip().replace("+", ""))


def extract_rows(md_path: Path) -> List[Row]:
    rows: List[Row] = []
    lines = md_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    in_table = False
    for line in lines:
        if line.startswith("| mode |") and "ΔPower(%)" in line:
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---|"):
            continue
        if not line.startswith("| "):
            if rows:
                break
            continue
        parts = [p.strip() for p in line.strip().split("|")[1:-1]]
        if len(parts) != 11:
            continue
        # mode, HPWL, ΔHPWL(%), Area, ΔArea(%), Power, ΔPower(%), WNS, ΔWNS(ns), TNS, ΔTNS(ns)
        rows.append(
            Row(
                mode=parts[0],
                d_hpwl_pct=parse_pct(parts[2]),
                d_area_pct=parse_pct(parts[4]),
                d_power_pct=parse_pct(parts[6]),
                d_wns_ns=parse_num(parts[8]),
                d_tns_ns=parse_num(parts[10]),
            )
        )
    return rows


def passes_goal_a(r: Row, target_power_delta_pct: float) -> bool:
    # Goal A: power down with no timing/area degradation.
    return (
        r.d_power_pct <= target_power_delta_pct
        and r.d_area_pct <= 0.0
        and r.d_wns_ns >= 0.0
        and r.d_tns_ns >= 0.0
    )


def milestone_level(r: Row) -> str:
    if r.d_area_pct > 0.0 or r.d_wns_ns < 0.0 or r.d_tns_ns < 0.0:
        return "M0"
    if r.d_power_pct <= -8.0:
        return "M4"
    if r.d_power_pct <= -5.0:
        return "M3"
    if r.d_power_pct <= -3.0:
        return "M2"
    if r.d_power_pct <= -1.0:
        return "M1"
    return "M0"


def rank_gap(r: Row, target_power_delta_pct: float) -> float:
    # Lower is better.
    p_gap = max(0.0, r.d_power_pct - target_power_delta_pct)
    area_pen = max(0.0, r.d_area_pct) * 1.5
    wns_pen = max(0.0, -r.d_wns_ns) * 10.0
    tns_pen = max(0.0, -r.d_tns_ns) / 50.0
    return p_gap + area_pen + wns_pen + tns_pen


def write_outputs(
    out_prefix: Path, rows: List[Row], target_power_delta_pct: float, target_freq_improve_pct: float
) -> None:
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    detail_tsv = out_prefix.with_suffix(".detail.tsv")
    summary_md = out_prefix.with_suffix(".summary.md")

    ranked = sorted(rows, key=lambda r: rank_gap(r, target_power_delta_pct))

    with detail_tsv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(
            [
                "mode",
                "delta_power_pct",
                "delta_area_pct",
                "delta_wns_ns",
                "delta_tns_ns",
                "goalA_pass",
                "goalA_gap_score",
                "milestone_level",
            ]
        )
        for r in ranked:
            w.writerow(
                [
                    r.mode,
                    f"{r.d_power_pct:.6f}",
                    f"{r.d_area_pct:.6f}",
                    f"{r.d_wns_ns:.6f}",
                    f"{r.d_tns_ns:.6f}",
                    "YES" if passes_goal_a(r, target_power_delta_pct) else "NO",
                    f"{rank_gap(r, target_power_delta_pct):.6f}",
                    milestone_level(r),
                ]
            )

    goal_a_pass = [r for r in ranked if passes_goal_a(r, target_power_delta_pct)]
    best_power = min(rows, key=lambda r: r.d_power_pct) if rows else None
    best_milestone = max(ranked, key=lambda r: ["M0", "M1", "M2", "M3", "M4"].index(milestone_level(r))) if ranked else None

    lines: List[str] = []
    lines.append("# BSPDN Goal Progress Summary")
    lines.append("")
    lines.append(f"- timestamp: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append(f"- target_goal_A: `delta_power_pct <= {target_power_delta_pct:.3f}% AND delta_area_pct<=0 AND delta_wns_ns>=0 AND delta_tns_ns>=0`")
    lines.append(f"- target_goal_B: `power/area non-worse + frequency improve >= {target_freq_improve_pct:.2f}%`")
    lines.append("- note_goal_B: `frequency-improve requires period sweep evidence; not inferable from single fixed-period PPA table.`")
    lines.append(f"- total_modes: `{len(rows)}`")
    lines.append(f"- goal_A_pass_count: `{len(goal_a_pass)}`")
    if best_milestone is not None:
        lines.append(f"- best_milestone_reached: `{milestone_level(best_milestone)}` by `{best_milestone.mode}`")
    if best_power is not None:
        lines.append(
            f"- best_power_mode: `{best_power.mode}` (delta_power_pct=`{best_power.d_power_pct:.3f}%`, delta_area_pct=`{best_power.d_area_pct:.3f}%`, delta_wns_ns=`{best_power.d_wns_ns:.3f}`, delta_tns_ns=`{best_power.d_tns_ns:.3f}`)"
        )
    lines.append("")
    lines.append("## Top-5 Nearest to Goal A")
    lines.append("| mode | dPower(%) | dArea(%) | dWNS(ns) | dTNS(ns) | gap_score |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for r in ranked[:5]:
        lines.append(
            f"| {r.mode} | {r.d_power_pct:.3f} | {r.d_area_pct:.3f} | {r.d_wns_ns:.3f} | {r.d_tns_ns:.3f} | {rank_gap(r, target_power_delta_pct):.3f} |"
        )
    lines.append("")
    lines.append("## Artifacts")
    lines.append(f"- detail_tsv: `{detail_tsv}`")
    lines.append(f"- summary_md: `{summary_md}`")
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    rows = extract_rows(Path(args.campaign_md))
    if not rows:
        raise SystemExit(f"no rows parsed from {args.campaign_md}")
    write_outputs(Path(args.out_prefix), rows, args.target_power_delta_pct, args.target_freq_improve_pct)
    print(f"wrote: {Path(args.out_prefix).with_suffix('.detail.tsv')}")
    print(f"wrote: {Path(args.out_prefix).with_suffix('.summary.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
