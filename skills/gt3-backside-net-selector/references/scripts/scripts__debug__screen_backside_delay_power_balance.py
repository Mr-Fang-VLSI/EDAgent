#!/usr/bin/env python3
"""Screen backside net candidates using delay + power crossover and critical-path safety.

Input TSV is expected from scripts/debug/backside_net_scorer.

Core model (L in um):
  tau_front(L) = 0.5*rf*cf*L^2 + rf*Cload*L
  tau_back (L) = 0.5*rb*cb*L^2 + (rb*Cload + 2*R_land*cb)*L + 2*R_land*(Cload + C_land)

  C_front(L) = cf*L + Cload
  C_back (L) = cb*L + Cload + 2*C_land

Selection gate:
  power_pass = (C_back <= C_front)
  delay_pass = (tau_back <= tau_front) OR (noncritical AND slack_ps - (tau_back-tau_front) >= slack_guard_ps)
  selected = power_pass AND delay_pass AND optional filters
"""

from __future__ import print_function

import argparse
import csv
import math
import os
from typing import Dict, List, Optional, Tuple


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report-tsv", required=True, help="backside_net_scorer report TSV")
    ap.add_argument("--out-prefix", required=True, help="output prefix (writes .tsv + .summary.md)")
    ap.add_argument("--dbu-per-um", type=float, default=2000.0)
    ap.add_argument("--c-unit-scale-to-pf", type=float, default=1e-3, help="scale factor for c-unit fields to pF/um")
    ap.add_argument("--c-load-pf", type=float, default=0.003)
    ap.add_argument("--front-r-scale", type=float, default=1.0)
    ap.add_argument("--back-r-scale", type=float, default=1.0)
    ap.add_argument("--front-c-scale", type=float, default=1.0)
    ap.add_argument("--back-c-scale", type=float, default=1.0)

    ap.add_argument("--r-ntsv-ohm", type=float, default=32.0)
    ap.add_argument("--r-front-via-ohm", type=float, default=4.0)
    ap.add_argument("--n-front-via-per-end", type=float, default=4.0)
    ap.add_argument("--r-back-via-ohm", type=float, default=4.0)
    ap.add_argument("--n-back-via-per-end", type=float, default=1.0)

    ap.add_argument("--c-ntsv-pf", type=float, default=2e-4)
    ap.add_argument("--c-front-via-pf", type=float, default=2e-5)
    ap.add_argument("--c-back-via-pf", type=float, default=2e-5)

    ap.add_argument("--criticality-file", default="", help="optional net/value table")
    ap.add_argument(
        "--criticality-type",
        default="slack",
        choices=["slack", "criticality"],
        help="value type in --criticality-file",
    )
    ap.add_argument("--criticality-threshold", type=float, default=0.30)
    ap.add_argument("--criticality-to-slack-ps", type=float, default=120.0)
    ap.add_argument("--default-slack-ps", type=float, default=0.0)
    ap.add_argument("--noncritical-slack-ps", type=float, default=40.0)
    ap.add_argument("--slack-guard-ps", type=float, default=5.0)

    ap.add_argument("--exclude-clock", action="store_true")
    ap.add_argument("--min-length-um", type=float, default=0.0)
    ap.add_argument(
        "--length-proxy",
        default="length",
        choices=["length", "hpwl", "max"],
        help="Which geometric proxy to use as L when routed length is unavailable",
    )
    return ap.parse_args()


def parse_float(s: str, default: float = 0.0) -> float:
    try:
        return float(s)
    except Exception:
        return default


def solve_delay_crossover(
    rf: float,
    cf: float,
    rb: float,
    cb: float,
    c_load: float,
    r_land: float,
    c_land: float,
) -> float:
    # Solve A*L^2 + B*L - C = 0 where delta = tau_front - tau_back.
    A = 0.5 * (rf * cf - rb * cb)
    B = (rf - rb) * c_load - 2.0 * r_land * cb
    C = 2.0 * r_land * (c_load + c_land)

    eps = 1e-14
    if abs(A) < eps:
        if abs(B) < eps:
            return float("inf")
        x = C / B
        return x if x > 0 else float("inf")

    disc = B * B + 4.0 * A * C
    if disc < 0:
        return float("inf")

    root = math.sqrt(disc)
    r1 = (-B + root) / (2.0 * A)
    r2 = (-B - root) / (2.0 * A)
    pos = [x for x in (r1, r2) if x > 0]
    if not pos:
        return float("inf")
    return min(pos)


def delay_front_ps(L_um: float, rf: float, cf: float, c_load: float) -> float:
    return 0.5 * rf * cf * L_um * L_um + rf * c_load * L_um


def delay_back_ps(
    L_um: float,
    rb: float,
    cb: float,
    c_load: float,
    r_land: float,
    c_land: float,
) -> float:
    return (
        0.5 * rb * cb * L_um * L_um
        + (rb * c_load + 2.0 * r_land * cb) * L_um
        + 2.0 * r_land * (c_load + c_land)
    )


def power_crossover(cf: float, cb: float, c_land: float) -> float:
    # C_back <= C_front -> (cf-cb)L >= 2*C_land
    d = cf - cb
    if d <= 1e-14:
        return float("inf")
    return (2.0 * c_land) / d


def read_criticality_map(path: str) -> Dict[str, float]:
    if not path:
        return {}
    out: Dict[str, float] = {}
    if not os.path.isfile(path):
        return out

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        first = f.readline()
        if not first:
            return out
        head_tokens = [x.strip().lower() for x in first.replace(",", "\t").split("\t")]
        has_header = ("net" in head_tokens)
        f.seek(0)
        if has_header:
            reader = csv.DictReader(f, delimiter="\t")
            if reader.fieldnames is None:
                return out
            val_key = None
            for k in reader.fieldnames:
                kl = k.lower()
                if kl in ("value", "slack", "slack_ps", "criticality"):
                    val_key = k
                    break
            if val_key is None and len(reader.fieldnames) >= 2:
                val_key = reader.fieldnames[1]
            if val_key is None:
                return out
            for row in reader:
                n = (row.get("net") or row.get("name") or "").strip()
                if not n:
                    continue
                out[n] = parse_float(row.get(val_key, ""), float("nan"))
            return out

        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            toks = line.replace(",", " ").split()
            if len(toks) < 2:
                continue
            out[toks[0]] = parse_float(toks[1], float("nan"))
    return out


def main() -> int:
    args = parse_args()

    crit_map = read_criticality_map(args.criticality_file)

    c_load = max(args.c_load_pf, 1e-12)
    r_land = (
        args.r_ntsv_ohm
        + args.n_front_via_per_end * args.r_front_via_ohm
        + args.n_back_via_per_end * args.r_back_via_ohm
    )
    c_land = (
        args.c_ntsv_pf
        + args.n_front_via_per_end * args.c_front_via_pf
        + args.n_back_via_per_end * args.c_back_via_pf
    )

    rows: List[Dict[str, object]] = []
    with open(args.report_tsv, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            net = (row.get("net") or "").strip()
            if not net:
                continue
            length_dbu = parse_float(row.get("length_dbu", "0"), 0.0)
            hpwl_dbu = parse_float(row.get("hpwl_dbu", "0"), 0.0)
            if args.length_proxy == "hpwl":
                L_dbu = hpwl_dbu
            elif args.length_proxy == "max":
                L_dbu = max(length_dbu, hpwl_dbu)
            else:
                L_dbu = length_dbu
            L_um = L_dbu / max(args.dbu_per_um, 1e-9)
            if L_um < args.min_length_um:
                continue

            use_clock = int(parse_float(row.get("use_clock", "0"), 0.0))
            if args.exclude_clock and use_clock == 1:
                continue

            rf = parse_float(row.get("current_r_unit", "0"), 0.0)
            rb = parse_float(row.get("backside_r_unit", "0"), 0.0)
            cf_raw = parse_float(row.get("current_c_unit", "0"), 0.0)
            cb_raw = parse_float(row.get("backside_c_unit", "0"), 0.0)
            cf = max(cf_raw * args.c_unit_scale_to_pf * args.front_c_scale, 1e-12)
            cb = max(cb_raw * args.c_unit_scale_to_pf * args.back_c_scale, 1e-12)
            rf = max(rf * args.front_r_scale, 1e-12)
            rb = max(rb * args.back_r_scale, 1e-12)

            l_delay = solve_delay_crossover(rf, cf, rb, cb, c_load, r_land, c_land)
            l_power = power_crossover(cf, cb, c_land)

            tf = delay_front_ps(L_um, rf, cf, c_load)
            tb = delay_back_ps(L_um, rb, cb, c_load, r_land, c_land)
            delta_ps = tb - tf

            cap_front = cf * L_um + c_load
            cap_back = cb * L_um + c_load + 2.0 * c_land
            delta_cap = cap_back - cap_front

            crit = parse_float(row.get("criticality", ""), float("nan"))
            if net in crit_map and args.criticality_type == "criticality":
                crit = crit_map[net]

            slack_ps: Optional[float] = None
            if net in crit_map and args.criticality_type == "slack":
                slack_ps = crit_map[net]
            elif math.isfinite(crit) and 0.0 <= crit <= 1.0 and args.criticality_to_slack_ps > 0:
                slack_ps = (1.0 - crit) * args.criticality_to_slack_ps
            else:
                slack_ps = args.default_slack_ps

            if math.isfinite(crit):
                noncritical = (crit <= args.criticality_threshold)
            else:
                noncritical = (slack_ps is not None and slack_ps >= args.noncritical_slack_ps)

            delay_direct_pass = (delta_ps <= 0.0)
            slack_safe = (slack_ps is not None and (slack_ps - delta_ps) >= args.slack_guard_ps)
            delay_pass = delay_direct_pass or (noncritical and slack_safe)
            power_pass = (delta_cap <= 0.0)
            selected = bool(delay_pass and power_pass)

            rows.append(
                {
                    "net": net,
                    "length_um": L_um,
                    "use_clock": use_clock,
                    "criticality": crit if math.isfinite(crit) else "NA",
                    "slack_ps": slack_ps if slack_ps is not None else "NA",
                    "rf_ohm_per_um": rf,
                    "rb_ohm_per_um": rb,
                    "cf_pF_per_um": cf,
                    "cb_pF_per_um": cb,
                    "lstar_delay_um": l_delay,
                    "lstar_power_um": l_power,
                    "tau_front_ps": tf,
                    "tau_back_ps": tb,
                    "delta_delay_ps": delta_ps,
                    "cap_front_pf": cap_front,
                    "cap_back_pf": cap_back,
                    "delta_cap_pf": delta_cap,
                    "delay_direct_pass": int(delay_direct_pass),
                    "noncritical": int(noncritical),
                    "slack_safe": int(slack_safe),
                    "delay_pass": int(delay_pass),
                    "power_pass": int(power_pass),
                    "selected": int(selected),
                }
            )

    rows.sort(
        key=lambda r: (
            -int(r["selected"]),
            -int(r["power_pass"]),
            -int(r["delay_pass"]),
            float(r["delta_cap_pf"]),
            float(r["delta_delay_ps"]),
        )
    )

    out_tsv = args.out_prefix + ".tsv"
    out_md = args.out_prefix + ".summary.md"

    fields = [
        "net",
        "length_um",
        "use_clock",
        "criticality",
        "slack_ps",
        "rf_ohm_per_um",
        "rb_ohm_per_um",
        "cf_pF_per_um",
        "cb_pF_per_um",
        "lstar_delay_um",
        "lstar_power_um",
        "tau_front_ps",
        "tau_back_ps",
        "delta_delay_ps",
        "cap_front_pf",
        "cap_back_pf",
        "delta_cap_pf",
        "delay_direct_pass",
        "noncritical",
        "slack_safe",
        "delay_pass",
        "power_pass",
        "selected",
    ]
    with open(out_tsv, "w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=fields, delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    n = len(rows)
    n_sel = sum(int(r["selected"]) for r in rows)
    n_pow = sum(int(r["power_pass"]) for r in rows)
    n_del = sum(int(r["delay_pass"]) for r in rows)
    n_slack = sum(int(r["slack_safe"]) for r in rows)

    top_rows = rows[:20]

    with open(out_md, "w", encoding="utf-8") as fo:
        fo.write("# Backside Delay+Power Balance Screening\n\n")
        fo.write("## Model\n")
        fo.write("- delay_front: `tau_f(L)=0.5*rf*cf*L^2 + rf*Cload*L`\n")
        fo.write("- delay_back: `tau_b(L)=0.5*rb*cb*L^2 + (rb*Cload+2*Rland*cb)*L + 2*Rland*(Cload+Cland)`\n")
        fo.write("- power proxy: `C_f(L)=cf*L+Cload`, `C_b(L)=cb*L+Cload+2*Cland`\n")
        fo.write("- select gate: `selected = power_pass AND (delay_direct OR (noncritical AND slack_safe))`\n\n")

        fo.write("## Parameters\n")
        fo.write("- c_load_pf: `{:.6f}`\n".format(c_load))
        fo.write("- r_land_ohm (per end): `{:.6f}`\n".format(r_land))
        fo.write("- c_land_pf (per end): `{:.6f}`\n".format(c_land))
        fo.write("- criticality_threshold: `{:.3f}`\n".format(args.criticality_threshold))
        fo.write("- slack_guard_ps: `{:.3f}`\n".format(args.slack_guard_ps))
        fo.write("- c_unit_scale_to_pf: `{:.6f}`\n".format(args.c_unit_scale_to_pf))
        fo.write("- front_r_scale/back_r_scale: `{:.3f}` / `{:.3f}`\n".format(args.front_r_scale, args.back_r_scale))
        fo.write("- front_c_scale/back_c_scale: `{:.3f}` / `{:.3f}`\n".format(args.front_c_scale, args.back_c_scale))
        fo.write("- exclude_clock: `{}`\n".format(int(args.exclude_clock)))
        fo.write("- min_length_um: `{:.3f}`\n\n".format(args.min_length_um))
        fo.write("- length_proxy: `{}`\n\n".format(args.length_proxy))

        fo.write("## Derivative Note\n")
        fo.write("- `d tau_f / dL = rf*cf*L + rf*Cload`\n")
        fo.write("- `d tau_b / dL = rb*cb*L + rb*Cload + 2*Rland*cb`\n")
        fo.write("- both forms are continuous and differentiable in `L` for fixed parameters.\n\n")

        fo.write("## Screening Summary\n")
        fo.write("- total_nets: `{}`\n".format(n))
        fo.write("- power_pass_nets: `{}`\n".format(n_pow))
        fo.write("- delay_pass_nets: `{}`\n".format(n_del))
        fo.write("- slack_safe_nets: `{}`\n".format(n_slack))
        fo.write("- selected_nets: `{}`\n\n".format(n_sel))

        fo.write("## Top Candidates (first 20)\n")
        fo.write("| net | L(um) | dDelay(ps) | dCap(pF) | L*_delay(um) | L*_power(um) | noncritical | slack_safe | selected |\n")
        fo.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for r in top_rows:
            fo.write(
                "| {} | {:.3f} | {:.4f} | {:.6f} | {} | {} | {} | {} | {} |\n".format(
                    r["net"],
                    float(r["length_um"]),
                    float(r["delta_delay_ps"]),
                    float(r["delta_cap_pf"]),
                    "inf" if not math.isfinite(float(r["lstar_delay_um"])) else "{:.3f}".format(float(r["lstar_delay_um"])),
                    "inf" if not math.isfinite(float(r["lstar_power_um"])) else "{:.3f}".format(float(r["lstar_power_um"])),
                    int(r["noncritical"]),
                    int(r["slack_safe"]),
                    int(r["selected"]),
                )
            )
        fo.write("\n")
        fo.write("- output_tsv: `{}`\n".format(out_tsv))

    print("total_nets={}".format(n))
    print("selected_nets={}".format(n_sel))
    print("out_tsv={}".format(out_tsv))
    print("out_md={}".format(out_md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
