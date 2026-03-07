#!/usr/bin/env python3
"""Power-first backside net selector for post-placement/postCTS DEFs.

Pipeline:
1. Run backside_net_scorer to build per-net geometry/PDK proxy report.
2. Run screen_backside_delay_power_balance.py to enforce power-first + timing-safe gate.
3. Rank selected nets by dynamic-power proxy and pick under backside capacity.
4. Emit reusable net list / escaped pattern list / summary artifacts.

If no activity file is provided, a uniform activity factor of 1.0 is assumed.
"""

from __future__ import annotations

import argparse
import csv
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Candidate:
    net: str
    pred_backside_dbu: int
    length_dbu: int
    use_clock: int
    delta_cap_pf: float
    delta_delay_ps: float
    slack_ps: float | None
    activity: float
    power_gain_proxy: float


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--def-file", required=True, help="Input DEF (typically postCTS/post-placement)")
    p.add_argument("--out-prefix", required=True, help="Artifact prefix")
    p.add_argument("--techlef-file", default="", help="Optional tech LEF for scorer timing proxy")
    p.add_argument("--model-mode", default="analytical", choices=["analytical", "route"], help="Scorer model mode")
    p.add_argument("--selection-mode", default="score", choices=["score", "density", "hybrid"], help="Scorer selection mode")
    p.add_argument("--capacity-ratio", type=float, default=0.08, help="Backside capacity ratio of total predicted demand")
    p.add_argument("--capacity-dbu", type=int, default=0, help="Absolute backside capacity in DBU")
    p.add_argument("--min-length-dbu", type=int, default=1000)
    p.add_argument("--report-topn", type=int, default=20000)
    p.add_argument("--topk-total", type=int, default=256)
    p.add_argument("--scorer-min-score", type=float, default=-1e30, help="Allow power-first flow to keep nets even if legacy scorer utility is negative")
    p.add_argument("--include-clock", action="store_true", help="Allow clock nets into final power-first selection")
    p.add_argument("--criticality-file", default="", help="Optional net/value table for power-balance screen")
    p.add_argument("--criticality-type", default="slack", choices=["slack", "criticality"])
    p.add_argument("--criticality-threshold", type=float, default=0.30)
    p.add_argument("--criticality-to-slack-ps", type=float, default=120.0)
    p.add_argument("--default-slack-ps", type=float, default=0.0)
    p.add_argument("--noncritical-slack-ps", type=float, default=40.0)
    p.add_argument("--slack-guard-ps", type=float, default=5.0)
    p.add_argument("--activity-file", default="", help="Optional net/activity table. If absent, use uniform activity=1.0")
    p.add_argument("--activity-default", type=float, default=1.0)
    p.add_argument("--activity-column", default="activity", help="Preferred activity column name when activity file has header")
    p.add_argument("--exclude-clock-in-screen", action="store_true", help="Also exclude clocks from delay+power screening stage")
    p.add_argument("--c-load-pf", type=float, default=0.003)
    p.add_argument("--c-unit-scale-to-pf", type=float, default=1e-3)
    p.add_argument("--r-ntsv-ohm", type=float, default=32.0)
    p.add_argument("--c-ntsv-pf", type=float, default=2e-4)
    p.add_argument("--screen-length-proxy", default="max", choices=["length", "hpwl", "max"])
    return p.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run(cmd: List[str]) -> None:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout)
        raise SystemExit(proc.returncode)


def ensure_scorer(root: Path) -> Path:
    scorer = root / "scripts/debug/backside_net_scorer"
    if scorer.is_file() and scorer.stat().st_mode & 0o111:
        return scorer
    run(["bash", str(root / "scripts/debug/build_backside_net_scorer.sh")])
    if not scorer.is_file():
        raise SystemExit(f"missing scorer binary after build: {scorer}")
    return scorer


def tcl_glob_escape(name: str) -> str:
    out: List[str] = []
    for ch in name:
        if ch in ("\\", "*", "?", "[", "]"):
            out.append("\\")
        out.append(ch)
    return "".join(out)


def read_activity_map(path: str, preferred_col: str, default: float) -> Dict[str, float]:
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"activity file not found: {path}")
    out: Dict[str, float] = {}
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        first = f.readline()
        if not first:
            return out
        has_header = "net" in first.lower()
        f.seek(0)
        if has_header:
            reader = csv.DictReader(f, delimiter="\t")
            if not reader.fieldnames:
                return out
            col = None
            for k in reader.fieldnames:
                if k.lower() == preferred_col.lower():
                    col = k
                    break
            if col is None:
                for k in reader.fieldnames:
                    if k.lower() in {"activity", "toggle", "toggle_rate", "alpha", "value"}:
                        col = k
                        break
            if col is None:
                if len(reader.fieldnames) < 2:
                    return out
                col = reader.fieldnames[1]
            for row in reader:
                net = (row.get("net") or row.get("name") or "").strip()
                if not net:
                    continue
                try:
                    out[net] = max(0.0, float(row.get(col, str(default))))
                except Exception:
                    out[net] = default
            return out
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            toks = line.replace(",", " ").split()
            if len(toks) < 2:
                continue
            try:
                out[toks[0]] = max(0.0, float(toks[1]))
            except Exception:
                out[toks[0]] = default
    return out


def parse_float(s: str, default: float = 0.0) -> float:
    try:
        return float(s)
    except Exception:
        return default


def read_scorer_report(path: Path) -> Dict[str, Dict[str, str]]:
    out: Dict[str, Dict[str, str]] = {}
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            net = (row.get("net") or "").strip()
            if net:
                out[net] = row
    return out


def read_power_screen(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows


def build_candidates(
    scorer: Dict[str, Dict[str, str]],
    screened: List[Dict[str, str]],
    activity_map: Dict[str, float],
    activity_default: float,
    include_clock: bool,
) -> List[Candidate]:
    out: List[Candidate] = []
    for row in screened:
        net = (row.get("net") or "").strip()
        if not net:
            continue
        if int(parse_float(row.get("selected", "0"), 0.0)) != 1:
            continue
        srow = scorer.get(net)
        if srow is None:
            continue
        use_clock = int(parse_float(srow.get("use_clock", "0"), 0.0))
        if use_clock and not include_clock:
            continue
        delta_cap_pf = parse_float(row.get("delta_cap_pf", "0"), 0.0)
        delta_delay_ps = parse_float(row.get("delta_delay_ps", "0"), 0.0)
        slack_raw = row.get("slack_ps", "")
        slack_ps = None if slack_raw in ("", "NA", None) else parse_float(slack_raw, 0.0)
        activity = activity_map.get(net, activity_default)
        power_gain_proxy = max(0.0, -delta_cap_pf) * max(0.0, activity)
        out.append(
            Candidate(
                net=net,
                pred_backside_dbu=max(1, int(parse_float(srow.get("pred_backside_dbu", "1"), 1.0))),
                length_dbu=max(0, int(parse_float(srow.get("length_dbu", "0"), 0.0))),
                use_clock=use_clock,
                delta_cap_pf=delta_cap_pf,
                delta_delay_ps=delta_delay_ps,
                slack_ps=slack_ps,
                activity=activity,
                power_gain_proxy=power_gain_proxy,
            )
        )
    out.sort(
        key=lambda c: (
            -c.power_gain_proxy,
            c.delta_delay_ps,
            -c.length_dbu,
            c.net,
        )
    )
    return out


def select_under_capacity(cands: List[Candidate], cap_dbu: int, topk_total: int) -> Tuple[List[Candidate], int]:
    picked: List[Candidate] = []
    used = 0
    for c in cands:
        if len(picked) >= topk_total:
            break
        if used + c.pred_backside_dbu > cap_dbu:
            continue
        picked.append(c)
        used += c.pred_backside_dbu
    return picked, used


def write_outputs(
    out_prefix: Path,
    selected: List[Candidate],
    all_candidates: List[Candidate],
    cap_dbu: int,
    used_dbu: int,
    scorer_report: Path,
    power_tsv: Path,
    power_md: Path,
    activity_file: str,
) -> None:
    nets_path = Path(str(out_prefix) + ".nets.txt")
    pat_path = Path(str(out_prefix) + ".patterns.txt")
    tsv_path = Path(str(out_prefix) + ".selection.tsv")
    md_path = Path(str(out_prefix) + ".summary.md")

    nets_path.parent.mkdir(parents=True, exist_ok=True)
    with nets_path.open("w", encoding="utf-8") as f:
        for c in selected:
            f.write(c.net + "\n")
    with pat_path.open("w", encoding="utf-8") as f:
        for c in selected:
            f.write(tcl_glob_escape(c.net) + "\n")
    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow([
            "rank", "net", "pred_backside_dbu", "length_dbu", "use_clock",
            "delta_cap_pf", "delta_delay_ps", "slack_ps", "activity", "power_gain_proxy"
        ])
        for i, c in enumerate(selected, start=1):
            w.writerow([
                i, c.net, c.pred_backside_dbu, c.length_dbu, c.use_clock,
                f"{c.delta_cap_pf:.9f}", f"{c.delta_delay_ps:.9f}",
                "NA" if c.slack_ps is None else f"{c.slack_ps:.9f}",
                f"{c.activity:.9f}", f"{c.power_gain_proxy:.9f}",
            ])
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Power-First Backside Net Selection\n\n")
        f.write(f"- scorer_report: `{scorer_report}`\n")
        f.write(f"- power_screen_tsv: `{power_tsv}`\n")
        f.write(f"- power_screen_summary: `{power_md}`\n")
        f.write(f"- activity_file: `{activity_file or 'uniform_activity=1.0'}`\n")
        f.write(f"- total_power_safe_candidates: `{len(all_candidates)}`\n")
        f.write(f"- selected_nets: `{len(selected)}`\n")
        f.write(f"- capacity_dbu: `{cap_dbu}`\n")
        f.write(f"- used_backside_dbu: `{used_dbu}`\n")
        f.write("\n")
        f.write("Selection objective: rank by `activity * max(0, -delta_cap_pf)` and keep timing-safe nets only.\n\n")
        f.write("| rank | net | dCap(pF) | dDelay(ps) | activity | power_gain_proxy | pred_backside_dbu | length_dbu | clock |\n")
        f.write("|---|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for i, c in enumerate(selected[:40], start=1):
            f.write(
                f"| {i} | {c.net} | {c.delta_cap_pf:.6f} | {c.delta_delay_ps:.4f} | {c.activity:.4f} | {c.power_gain_proxy:.6f} | {c.pred_backside_dbu} | {c.length_dbu} | {c.use_clock} |\n"
            )


def main() -> int:
    args = parse_args()
    root = repo_root()
    scorer_bin = ensure_scorer(root)
    out_prefix = Path(args.out_prefix).resolve()
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    scorer_prefix = Path(str(out_prefix) + ".scorer")
    power_prefix = Path(str(out_prefix) + ".power")
    scorer_report = Path(str(scorer_prefix) + ".report.tsv")
    power_tsv = Path(str(power_prefix) + ".tsv")
    power_md = Path(str(power_prefix) + ".summary.md")

    scorer_cmd = [
        str(scorer_bin),
        f"--def-file={Path(args.def_file).resolve()}",
        f"--out-nets={str(scorer_prefix)}.nets.txt",
        f"--out-report={scorer_report}",
        f"--model-mode={args.model_mode}",
        f"--selection-mode={args.selection_mode}",
        f"--topk={args.report_topn}",
        f"--report-topn={args.report_topn}",
        f"--capacity-ratio={args.capacity_ratio}",
        f"--min-length-dbu={args.min_length_dbu}",
        f"--min-score={args.scorer_min_score}",
    ]
    if args.techlef_file:
        scorer_cmd.append(f"--techlef-file={Path(args.techlef_file).resolve()}")
    if args.include_clock:
        scorer_cmd.append("--include-clock")
    run(scorer_cmd)

    power_cmd = [
        sys.executable,
        str(root / "scripts/debug/screen_backside_delay_power_balance.py"),
        "--report-tsv", str(scorer_report),
        "--out-prefix", str(power_prefix),
        "--min-length-um", str(args.min_length_dbu / 2000.0),
        "--c-load-pf", str(args.c_load_pf),
        "--c-unit-scale-to-pf", str(args.c_unit_scale_to_pf),
        "--r-ntsv-ohm", str(args.r_ntsv_ohm),
        "--c-ntsv-pf", str(args.c_ntsv_pf),
        "--criticality-type", args.criticality_type,
        "--criticality-threshold", str(args.criticality_threshold),
        "--criticality-to-slack-ps", str(args.criticality_to_slack_ps),
        "--default-slack-ps", str(args.default_slack_ps),
        "--noncritical-slack-ps", str(args.noncritical_slack_ps),
        "--slack-guard-ps", str(args.slack_guard_ps),
        "--length-proxy", args.screen_length_proxy,
    ]
    if args.criticality_file:
        power_cmd.extend(["--criticality-file", str(Path(args.criticality_file).resolve())])
    if args.exclude_clock_in_screen:
        power_cmd.append("--exclude-clock")
    run(power_cmd)

    scorer_map = read_scorer_report(scorer_report)
    screened_rows = read_power_screen(power_tsv)
    activity_map = read_activity_map(args.activity_file, args.activity_column, args.activity_default)
    candidates = build_candidates(
        scorer_map,
        screened_rows,
        activity_map,
        args.activity_default,
        args.include_clock,
    )
    total_pred = sum(max(1, int(parse_float(row.get("pred_backside_dbu", "1"), 1.0))) for row in scorer_map.values())
    cap_dbu = args.capacity_dbu if args.capacity_dbu > 0 else int(round(total_pred * args.capacity_ratio))
    if cap_dbu <= 0:
        raise SystemExit("computed backside capacity is non-positive")
    selected, used_dbu = select_under_capacity(candidates, cap_dbu, args.topk_total)
    write_outputs(out_prefix, selected, candidates, cap_dbu, used_dbu, scorer_report, power_tsv, power_md, args.activity_file)

    print(f"scorer_report={scorer_report}")
    print(f"power_screen_tsv={power_tsv}")
    print(f"selected_nets={len(selected)}")
    print(f"selection_summary={str(out_prefix)}.summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
