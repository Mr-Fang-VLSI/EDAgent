#!/usr/bin/env python3
"""Build a bucketed scorecard for model-vs-HPWL delay consistency."""

from __future__ import annotations

import argparse
import csv
import math
import pathlib
from collections import defaultdict
from typing import Dict, List, Tuple


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-tsv", default="", help="Unified TSV with merged fields")
    ap.add_argument("--target-tsv", default="", help="Target TSV (tau/delta)")
    ap.add_argument("--model-tsv", default="", help="Model TSV (cost/hpwl/fanout/tsv-proxy)")
    ap.add_argument("--key-col", default="net")
    ap.add_argument(
        "--delta-sign",
        choices=["back_minus_front", "front_minus_back"],
        default="back_minus_front",
    )
    ap.add_argument("--len-quantiles", default="0.33,0.66")
    ap.add_argument("--fanout-quantiles", default="0.33,0.66")
    ap.add_argument("--tsv-quantiles", default="0.33,0.66")
    ap.add_argument("--min-bucket-n", type=int, default=20)
    ap.add_argument("--key-len-thr", type=float, default=0.66, help="Quantile threshold for key long bucket")
    ap.add_argument("--key-fo-thr", type=float, default=0.66, help="Quantile threshold for key fanout bucket")
    ap.add_argument("--out-prefix", required=True)
    return ap.parse_args()


def read_tsv(path: pathlib.Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def to_float(x: str) -> float:
    try:
        return float(x)
    except Exception:
        return float("nan")


def pick_alias(row: Dict[str, str], aliases: List[str]) -> float:
    for a in aliases:
        if a in row and row[a] != "":
            v = to_float(row[a])
            if math.isfinite(v):
                return v
    return float("nan")


ALIASES = {
    "tau_front_ps": ["tau_front_ps", "front_tau_ps", "front_max_tau_ps", "front_mean_tau_ps"],
    "tau_back_ps": ["tau_back_ps", "back_tau_ps", "back_max_tau_ps", "back_mean_tau_ps"],
    "delta_tau_ps": ["delta_tau_ps", "delta_max_tau_ps", "delta_mean_tau_ps"],
    "cost_front": ["cost_front", "front_cost", "model_cost_front"],
    "cost_back": ["cost_back", "back_cost", "model_cost_back"],
    "delta_cost": ["delta_cost", "model_delta_cost", "pdk_timing_raw"],
    "pin_hpwl": ["pin_hpwl_um", "pin_hpwl", "hpwl_um", "hpwl_dbu"],
    "route_len": ["route_len_um", "route_len", "length_um", "length_dbu", "length_dbu_front", "length_dbu_back"],
    "fanout": ["fanout", "fanout_n", "pin_count", "sink_count", "front_sink_count"],
    "tsv_proxy": ["min_ntsv", "nearest_tsv_um", "pdk_via_proxy_raw", "pdk_via_proxy_n", "ntsv_count"],
}


def sign(v: float, eps: float = 1e-12) -> int:
    if not math.isfinite(v):
        return 0
    if v > eps:
        return 1
    if v < -eps:
        return -1
    return 0


def pearson(xs: List[float], ys: List[float]) -> float:
    n = len(xs)
    if n < 3:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0 or vy <= 0:
        return float("nan")
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / math.sqrt(vx * vy)


def rank(vals: List[float]) -> List[float]:
    order = sorted((v, i) for i, v in enumerate(vals))
    out = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and order[j + 1][0] == order[i][0]:
            j += 1
        rv = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            out[order[k][1]] = rv
        i = j + 1
    return out


def spearman(xs: List[float], ys: List[float]) -> float:
    return pearson(rank(xs), rank(ys))


def quantile(vals: List[float], q: float) -> float:
    if not vals:
        return float("nan")
    s = sorted(vals)
    i = max(0, min(len(s) - 1, int(math.floor(q * (len(s) - 1)))))
    return s[i]


def parse_qpair(s: str) -> Tuple[float, float]:
    xs = [to_float(x.strip()) for x in s.split(",")]
    if len(xs) != 2 or not all(math.isfinite(x) for x in xs):
        raise SystemExit(f"ERROR: invalid quantile pair: {s}")
    a, b = sorted(xs)
    return a, b


def merge_rows(args: argparse.Namespace) -> List[Dict[str, str]]:
    if args.input_tsv:
        return read_tsv(pathlib.Path(args.input_tsv))
    if not args.target_tsv or not args.model_tsv:
        raise SystemExit("ERROR: provide --input-tsv or both --target-tsv and --model-tsv")
    trows = read_tsv(pathlib.Path(args.target_tsv))
    mrows = read_tsv(pathlib.Path(args.model_tsv))
    k = args.key_col
    md = {r.get(k, ""): r for r in mrows if r.get(k, "")}
    out: List[Dict[str, str]] = []
    for tr in trows:
        key = tr.get(k, "")
        if not key:
            continue
        rr = dict(tr)
        if key in md:
            for kk, vv in md[key].items():
                if kk == k:
                    continue
                rr[kk] = vv
        out.append(rr)
    return out


def main() -> int:
    args = parse_args()
    lq0, lq1 = parse_qpair(args.len_quantiles)
    fq0, fq1 = parse_qpair(args.fanout_quantiles)
    tq0, tq1 = parse_qpair(args.tsv_quantiles)

    rows = merge_rows(args)
    out_prefix = pathlib.Path(args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    out_tsv = out_prefix.with_suffix(".bucketed.tsv")
    out_md = out_prefix.with_suffix(".bucketed.md")
    out_pts = out_prefix.with_suffix(".points.tsv")

    pts = []
    for r in rows:
        tf = pick_alias(r, ALIASES["tau_front_ps"])
        tb = pick_alias(r, ALIASES["tau_back_ps"])
        dt = pick_alias(r, ALIASES["delta_tau_ps"])
        if not math.isfinite(dt) and math.isfinite(tf) and math.isfinite(tb):
            dt = (tb - tf) if args.delta_sign == "back_minus_front" else (tf - tb)

        cf = pick_alias(r, ALIASES["cost_front"])
        cb = pick_alias(r, ALIASES["cost_back"])
        dc = pick_alias(r, ALIASES["delta_cost"])
        if not math.isfinite(dc) and math.isfinite(cf) and math.isfinite(cb):
            dc = (cb - cf) if args.delta_sign == "back_minus_front" else (cf - cb)

        hpwl = pick_alias(r, ALIASES["pin_hpwl"])
        rlen = pick_alias(r, ALIASES["route_len"])
        fanout = pick_alias(r, ALIASES["fanout"])
        tsv = pick_alias(r, ALIASES["tsv_proxy"])

        pts.append(
            {
                args.key_col: r.get(args.key_col, ""),
                "delta_tau_ps": dt,
                "abs_delta_tau_ps": abs(dt) if math.isfinite(dt) else float("nan"),
                "delta_cost": dc,
                "abs_delta_cost": abs(dc) if math.isfinite(dc) else float("nan"),
                "pin_hpwl": hpwl,
                "route_len": rlen,
                "fanout": fanout,
                "tsv_proxy": tsv,
            }
        )

    valid_bucket = [p for p in pts if math.isfinite(p["pin_hpwl"]) and math.isfinite(p["fanout"]) and math.isfinite(p["tsv_proxy"])]
    if not valid_bucket:
        raise SystemExit("ERROR: no rows with finite pin_hpwl/fanout/tsv_proxy")

    len_q0 = quantile([p["pin_hpwl"] for p in valid_bucket], lq0)
    len_q1 = quantile([p["pin_hpwl"] for p in valid_bucket], lq1)
    fo_q0 = quantile([p["fanout"] for p in valid_bucket], fq0)
    fo_q1 = quantile([p["fanout"] for p in valid_bucket], fq1)
    tsv_q0 = quantile([p["tsv_proxy"] for p in valid_bucket], tq0)
    tsv_q1 = quantile([p["tsv_proxy"] for p in valid_bucket], tq1)

    def bucket(v: float, q0: float, q1: float, names: Tuple[str, str, str]) -> str:
        if not math.isfinite(v):
            return "na"
        if v <= q0:
            return names[0]
        if v <= q1:
            return names[1]
        return names[2]

    for p in pts:
        p["len_bucket"] = bucket(p["pin_hpwl"], len_q0, len_q1, ("short", "mid", "long"))
        p["fanout_bucket"] = bucket(p["fanout"], fo_q0, fo_q1, ("fo_low", "fo_mid", "fo_high"))
        p["tsv_bucket"] = bucket(p["tsv_proxy"], tsv_q0, tsv_q1, ("tsv_low", "tsv_mid", "tsv_high"))
        p["bucket3d"] = f"{p['len_bucket']}|{p['fanout_bucket']}|{p['tsv_bucket']}"

    # Write points with buckets.
    pf = [
        args.key_col,
        "delta_tau_ps",
        "abs_delta_tau_ps",
        "delta_cost",
        "abs_delta_cost",
        "pin_hpwl",
        "route_len",
        "fanout",
        "tsv_proxy",
        "len_bucket",
        "fanout_bucket",
        "tsv_bucket",
        "bucket3d",
    ]
    with out_pts.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=pf, delimiter="\t")
        w.writeheader()
        for p in pts:
            rr = {k: p[k] for k in pf}
            for k in rr:
                if isinstance(rr[k], float):
                    rr[k] = f"{rr[k]:.6g}" if math.isfinite(rr[k]) else "NA"
            w.writerow(rr)

    groups: Dict[str, List[Dict[str, float]]] = defaultdict(list)
    for p in pts:
        if "na" in p["bucket3d"]:
            continue
        groups[p["bucket3d"]].append(p)

    recs = []
    for g, gp in sorted(groups.items()):
        if len(gp) < args.min_bucket_n:
            continue
        pairs_dc_tau = [
            (x["delta_cost"], x["delta_tau_ps"])
            for x in gp
            if math.isfinite(x["delta_cost"]) and math.isfinite(x["delta_tau_ps"])
        ]
        dc = [a for a, _ in pairs_dc_tau]
        dt = [b for _, b in pairs_dc_tau]

        pairs_hp_tau = [
            (x["pin_hpwl"], x["abs_delta_tau_ps"])
            for x in gp
            if math.isfinite(x["pin_hpwl"]) and math.isfinite(x["abs_delta_tau_ps"])
        ]
        hp = [a for a, _ in pairs_hp_tau]
        at_hp = [b for _, b in pairs_hp_tau]

        pairs_rl_tau = [
            (x["route_len"], x["abs_delta_tau_ps"])
            for x in gp
            if math.isfinite(x["route_len"]) and math.isfinite(x["abs_delta_tau_ps"])
        ]
        rl = [a for a, _ in pairs_rl_tau]
        at_rl = [b for _, b in pairs_rl_tau]

        pairs_absdc_tau = [
            (abs(x["delta_cost"]), x["abs_delta_tau_ps"])
            for x in gp
            if math.isfinite(x["delta_cost"]) and math.isfinite(x["abs_delta_tau_ps"])
        ]
        abs_dc = [a for a, _ in pairs_absdc_tau]
        at_dc = [b for _, b in pairs_absdc_tau]

        nz = [(x["delta_cost"], x["delta_tau_ps"]) for x in gp if sign(x["delta_cost"]) != 0 and sign(x["delta_tau_ps"]) != 0]
        sign_acc = (sum(1 for a, b in nz if sign(a) == sign(b)) / len(nz)) if nz else float("nan")

        p_abs_model = pearson(abs_dc, at_dc) if len(abs_dc) >= 3 else float("nan")
        p_abs_hpwl = pearson(hp, at_hp) if len(hp) >= 3 else float("nan")
        p_abs_rlen = pearson(rl, at_rl) if len(rl) >= 3 else float("nan")
        s_abs_model = spearman(abs_dc, at_dc) if len(abs_dc) >= 3 else float("nan")
        s_abs_hpwl = spearman(hp, at_hp) if len(hp) >= 3 else float("nan")
        s_abs_rlen = spearman(rl, at_rl) if len(rl) >= 3 else float("nan")

        p_delta = pearson(dc, dt) if len(dc) >= 3 else float("nan")
        s_delta = spearman(dc, dt) if len(dc) >= 3 else float("nan")

        model_win = (
            math.isfinite(s_abs_model)
            and math.isfinite(s_abs_hpwl)
            and abs(s_abs_model) > abs(s_abs_hpwl)
        )

        lb, fb, tb = g.split("|")
        recs.append(
            {
                "bucket3d": g,
                "len_bucket": lb,
                "fanout_bucket": fb,
                "tsv_bucket": tb,
                "n": len(gp),
                "pearson_delta_cost_vs_delta_tau": p_delta,
                "spearman_delta_cost_vs_delta_tau": s_delta,
                "sign_accuracy": sign_acc,
                "pearson_abs_model_vs_abs_tau": p_abs_model,
                "spearman_abs_model_vs_abs_tau": s_abs_model,
                "pearson_hpwl_vs_abs_tau": p_abs_hpwl,
                "spearman_hpwl_vs_abs_tau": s_abs_hpwl,
                "pearson_rlen_vs_abs_tau": p_abs_rlen,
                "spearman_rlen_vs_abs_tau": s_abs_rlen,
                "model_beats_hpwl_abs": "1" if model_win else "0",
            }
        )

    # Add a global row.
    gp = [p for p in pts if math.isfinite(p["delta_tau_ps"]) and math.isfinite(p["pin_hpwl"])]
    if gp:
        pairs_dc_tau = [
            (x["delta_cost"], x["delta_tau_ps"])
            for x in gp
            if math.isfinite(x["delta_cost"]) and math.isfinite(x["delta_tau_ps"])
        ]
        dc = [a for a, _ in pairs_dc_tau]
        dt = [b for _, b in pairs_dc_tau]

        pairs_absdc_tau = [
            (abs(x["delta_cost"]), x["abs_delta_tau_ps"])
            for x in gp
            if math.isfinite(x["delta_cost"]) and math.isfinite(x["abs_delta_tau_ps"])
        ]
        abs_dc = [a for a, _ in pairs_absdc_tau]
        abs_tau = [b for _, b in pairs_absdc_tau]

        pairs_hp_tau = [
            (x["pin_hpwl"], x["abs_delta_tau_ps"])
            for x in gp
            if math.isfinite(x["pin_hpwl"]) and math.isfinite(x["abs_delta_tau_ps"])
        ]
        hp = [a for a, _ in pairs_hp_tau]
        at_hp = [b for _, b in pairs_hp_tau]

        pairs_rl_tau = [
            (x["route_len"], x["abs_delta_tau_ps"])
            for x in gp
            if math.isfinite(x["route_len"]) and math.isfinite(x["abs_delta_tau_ps"])
        ]
        rl = [a for a, _ in pairs_rl_tau]
        at_rl = [b for _, b in pairs_rl_tau]
        nz = [(x["delta_cost"], x["delta_tau_ps"]) for x in gp if sign(x["delta_cost"]) != 0 and sign(x["delta_tau_ps"]) != 0]
        sign_acc = (sum(1 for a, b in nz if sign(a) == sign(b)) / len(nz)) if nz else float("nan")
        recs.append(
            {
                "bucket3d": "GLOBAL",
                "len_bucket": "all",
                "fanout_bucket": "all",
                "tsv_bucket": "all",
                "n": len(gp),
                "pearson_delta_cost_vs_delta_tau": pearson(dc, dt) if len(dc) >= 3 else float("nan"),
                "spearman_delta_cost_vs_delta_tau": spearman(dc, dt) if len(dc) >= 3 else float("nan"),
                "sign_accuracy": sign_acc,
                "pearson_abs_model_vs_abs_tau": pearson(abs_dc, abs_tau) if len(abs_dc) >= 3 else float("nan"),
                "spearman_abs_model_vs_abs_tau": spearman(abs_dc, abs_tau) if len(abs_dc) >= 3 else float("nan"),
                "pearson_hpwl_vs_abs_tau": pearson(hp, at_hp) if len(hp) >= 3 else float("nan"),
                "spearman_hpwl_vs_abs_tau": spearman(hp, at_hp) if len(hp) >= 3 else float("nan"),
                "pearson_rlen_vs_abs_tau": pearson(rl, at_rl) if len(rl) >= 3 else float("nan"),
                "spearman_rlen_vs_abs_tau": spearman(rl, at_rl) if len(rl) >= 3 else float("nan"),
                "model_beats_hpwl_abs": "1"
                if math.isfinite(spearman(abs_dc, abs_tau))
                and math.isfinite(spearman(hp, at_hp))
                and abs(spearman(abs_dc, abs_tau)) > abs(spearman(hp, at_hp))
                else "0",
            }
        )

    fields = [
        "bucket3d",
        "len_bucket",
        "fanout_bucket",
        "tsv_bucket",
        "n",
        "pearson_delta_cost_vs_delta_tau",
        "spearman_delta_cost_vs_delta_tau",
        "sign_accuracy",
        "pearson_abs_model_vs_abs_tau",
        "spearman_abs_model_vs_abs_tau",
        "pearson_hpwl_vs_abs_tau",
        "spearman_hpwl_vs_abs_tau",
        "pearson_rlen_vs_abs_tau",
        "spearman_rlen_vs_abs_tau",
        "model_beats_hpwl_abs",
    ]
    with out_tsv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        for r in recs:
            rr = dict(r)
            for k, v in rr.items():
                if isinstance(v, float):
                    rr[k] = f"{v:.4f}" if math.isfinite(v) else "NA"
            w.writerow(rr)

    # Key buckets: long + high fanout (tsv any) based on quantile labeling.
    key_rows = [r for r in recs if r["len_bucket"] == "long" and r["fanout_bucket"] == "fo_high"]
    key_n = sum(int(r["n"]) for r in key_rows)
    key_win = sum(1 for r in key_rows if r["model_beats_hpwl_abs"] == "1")
    key_total = len(key_rows)

    lines = [
        "# Bucketed Delay-Model Scorecard",
        "",
        f"- rows_total: `{len(rows)}`",
        f"- rows_points: `{len(pts)}`",
        f"- min_bucket_n: `{args.min_bucket_n}`",
        "",
        "## Quantile Boundaries",
        "",
        f"- length_q: q0={lq0:.2f} ({len_q0:.6g}), q1={lq1:.2f} ({len_q1:.6g})",
        f"- fanout_q: q0={fq0:.2f} ({fo_q0:.6g}), q1={fq1:.2f} ({fo_q1:.6g})",
        f"- tsv_q: q0={tq0:.2f} ({tsv_q0:.6g}), q1={tq1:.2f} ({tsv_q1:.6g})",
        "",
        "## Key Bucket Summary (long + high fanout)",
        "",
        f"- key_bucket_rows: `{key_total}`",
        f"- key_bucket_total_n: `{key_n}`",
        f"- key_bucket_model_beats_hpwl_rows: `{key_win}`",
        "",
        "## Outputs",
        f"- points_tsv: `{out_pts}`",
        f"- bucketed_tsv: `{out_tsv}`",
        f"- summary_md: `{out_md}`",
    ]
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(out_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
