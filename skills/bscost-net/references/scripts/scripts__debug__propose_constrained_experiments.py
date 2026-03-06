#!/usr/bin/env python3
"""Propose next experiment settings from memory DB under constraints."""

import argparse
import csv
import json
import math
import pathlib
import sqlite3
from typing import Dict, List, Optional, Tuple


DEFAULT_DB = "regression/experiment_memory/experiment_memory.db"


def to_float(v: str) -> Optional[float]:
    if v is None:
        return None
    s = str(v).strip()
    if s == "" or s.upper() in {"NA", "N/A", "NONE", "-"}:
        return None
    try:
        return float(s)
    except Exception:
        return None


def load_candidates(path: pathlib.Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        rd = csv.DictReader(f, delimiter="\t")
        return list(rd)


def candidate_id(row: Dict[str, str], idx: int) -> str:
    for k in ("setting_id", "id", "name", "variant", "mode", "tag"):
        v = (row.get(k) or "").strip()
        if v:
            return v
    return "cand_{:03d}".format(idx + 1)


def parse_param_json(s: str) -> Dict[str, str]:
    if not s:
        return {}
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            out = {}
            for k, v in obj.items():
                out[str(k)] = str(v)
            return out
    except Exception:
        pass
    return {}


def derive_setting_id_from_mode(mode: str) -> str:
    m = (mode or "").strip()
    if not m:
        return ""
    if ":" in m:
        return m.split(":", 1)[0].strip()
    return ""


def key_from_row(row: Dict[str, str], key_cols: List[str]) -> Tuple[Tuple[str, str], ...]:
    pairs = []
    for k in key_cols:
        v = (row.get(k) or "").strip()
        if (not v) and k == "mode":
            v = (row.get("setting_id") or "").strip()
        if (not v) and k in {"setting_id", "id"}:
            v = (row.get("mode") or "").strip()
        pairs.append((k, v))
    return tuple(pairs)


def key_from_history(mode: str, param_map: Dict[str, str], key_cols: List[str]) -> Tuple[Tuple[str, str], ...]:
    pairs = []
    for k in key_cols:
        v = (param_map.get(k) or "").strip()
        if (not v) and k == "mode":
            v = (mode or "").strip()
        if (not v) and k in {"setting_id", "id"}:
            v = derive_setting_id_from_mode(mode)
        pairs.append((k, v))
    return tuple(pairs)


def mean_std(vals: List[float]) -> Tuple[float, float]:
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / float(len(vals))
    if len(vals) == 1:
        return m, 0.0
    var = sum((x - m) ** 2 for x in vals) / float(len(vals) - 1)
    return m, math.sqrt(max(0.0, var))


def query_history(
    conn: sqlite3.Connection,
    design: str,
    phase: str,
    objective: str,
    wns_min: Optional[float],
    runtime_max: Optional[float],
) -> List[dict]:
    sql = (
        "SELECT mode, param_json, {} AS obj, wns_ns, runtime_sec, success "
        "FROM experiment_rows WHERE design=? AND phase=? AND success=1"
    ).format(objective)
    args: List[object] = [design, phase]
    if wns_min is not None:
        sql += " AND (wns_ns IS NULL OR wns_ns>=?)"
        args.append(wns_min)
    if runtime_max is not None:
        sql += " AND (runtime_sec IS NULL OR runtime_sec<=?)"
        args.append(runtime_max)
    sql += " AND {} IS NOT NULL".format(objective)
    cur = conn.execute(sql, args)
    out = []
    for mode, pj, obj, wns, runtime_sec, success in cur.fetchall():
        out.append(
            {
                "mode": "" if mode is None else str(mode),
                "param_map": parse_param_json(pj or ""),
                "objective": float(obj),
                "wns": None if wns is None else float(wns),
                "runtime_sec": None if runtime_sec is None else float(runtime_sec),
                "success": int(success),
            }
        )
    return out


def render_md(
    out_md: pathlib.Path,
    design: str,
    phase: str,
    objective: str,
    direction: str,
    rows: List[Dict[str, str]],
) -> None:
    lines = [
        "# Autonomous Experiment Proposal",
        "",
        "- design: `{}`".format(design),
        "- phase: `{}`".format(phase),
        "- objective: `{}` ({})".format(objective, direction),
        "- proposed_rows: `{}`".format(len(rows)),
        "",
        "| rank | candidate_id | predicted_obj | score | history_n | key |",
        "|---:|---|---:|---:|---:|---|",
    ]
    for i, r in enumerate(rows, start=1):
        lines.append(
            "| {} | {} | {} | {} | {} | {} |".format(
                i,
                r["candidate_id"],
                r["predicted_obj"],
                r["score"],
                r["history_n"],
                r["key"],
            )
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[2]
    ap = argparse.ArgumentParser(description="Propose next settings under constraints from experiment memory")
    ap.add_argument("--db", default=str((root / DEFAULT_DB).resolve()))
    ap.add_argument("--candidates", required=True, help="Candidate settings TSV")
    ap.add_argument("--design", required=True)
    ap.add_argument("--phase", default="route")
    ap.add_argument("--objective", default="power_mw", choices=["power_mw", "hpwl_um", "area_um2", "wns_ns", "tns_ns", "runtime_sec"])
    ap.add_argument("--direction", default="min", choices=["min", "max"])
    ap.add_argument("--key-cols", default="mode", help="Comma-separated parameter columns used for history matching")
    ap.add_argument("--wns-min", type=float, default=None)
    ap.add_argument("--runtime-max", type=float, default=None)
    ap.add_argument("--explore-lambda", type=float, default=0.35)
    ap.add_argument("--topk", type=int, default=10)
    ap.add_argument("--out-tsv", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    db = pathlib.Path(args.db).resolve()
    cand_path = pathlib.Path(args.candidates).resolve()
    out_tsv = pathlib.Path(args.out_tsv).resolve()
    out_md = pathlib.Path(args.out_md).resolve()
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db))
    hist = query_history(
        conn=conn,
        design=args.design,
        phase=args.phase,
        objective=args.objective,
        wns_min=args.wns_min,
        runtime_max=args.runtime_max,
    )
    conn.close()

    global_vals = [h["objective"] for h in hist]
    g_mean, g_std = mean_std(global_vals if global_vals else [0.0])
    if g_std <= 0.0:
        g_std = max(1e-6, abs(g_mean) * 0.05 + 1e-3)

    key_cols = [x.strip() for x in args.key_cols.split(",") if x.strip()]
    if not key_cols:
        key_cols = ["mode"]

    hist_by_key: Dict[Tuple[Tuple[str, str], ...], List[float]] = {}
    for h in hist:
        k = key_from_history(h.get("mode", ""), h["param_map"], key_cols)
        hist_by_key.setdefault(k, []).append(h["objective"])

    candidates = load_candidates(cand_path)
    ranked: List[Dict[str, str]] = []
    for i, row in enumerate(candidates):
        cid = candidate_id(row, i)
        key = key_from_row(row, key_cols)
        vals = hist_by_key.get(key, [])
        n = len(vals)
        if n > 0:
            mu, sd = mean_std(vals)
        else:
            mu, sd = g_mean, g_std
        if sd <= 0.0:
            sd = g_std

        # UCB-like score: better mean + exploration bonus.
        explore = args.explore_lambda * g_std / math.sqrt(float(n + 1))
        if args.direction == "min":
            score = -mu + explore
        else:
            score = mu + explore

        ranked.append(
            {
                "candidate_id": cid,
                "score_f": score,
                "predicted_obj_f": mu,
                "history_n_i": n,
                "key": "|".join("{}={}".format(k0, v0) for k0, v0 in key),
                "row": row,
            }
        )

    ranked.sort(key=lambda x: x["score_f"], reverse=True)
    ranked = ranked[: max(1, args.topk)]

    fields = ["rank", "candidate_id", "predicted_obj", "score", "history_n", "key"]
    with out_tsv.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        wr.writeheader()
        for ridx, r in enumerate(ranked, start=1):
            wr.writerow(
                {
                    "rank": ridx,
                    "candidate_id": r["candidate_id"],
                    "predicted_obj": "{:.6g}".format(r["predicted_obj_f"]),
                    "score": "{:.6g}".format(r["score_f"]),
                    "history_n": r["history_n_i"],
                    "key": r["key"],
                }
            )

    md_rows: List[Dict[str, str]] = []
    for r in ranked:
        md_rows.append(
            {
                "candidate_id": r["candidate_id"],
                "predicted_obj": "{:.6g}".format(r["predicted_obj_f"]),
                "score": "{:.6g}".format(r["score_f"]),
                "history_n": str(r["history_n_i"]),
                "key": r["key"],
            }
        )
    render_md(
        out_md=out_md,
        design=args.design,
        phase=args.phase,
        objective=args.objective,
        direction=args.direction,
        rows=md_rows,
    )

    print("db={}".format(db))
    print("history_rows={}".format(len(hist)))
    print("out_tsv={}".format(out_tsv))
    print("out_md={}".format(out_md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
