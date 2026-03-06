#!/usr/bin/env python3
"""Dual gate for backside cost model:
1) delay-consistency gate vs HPWL and absolute floors,
2) nTSV-capacity overflow behavior gate.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import RepeatedKFold


DEFAULT_DATASETS = [
    (
        "validate_20260228_1",
        "slurm_logs/04_delay_modeling/backside_delay_model_validate_20260228_1.delay.tsv",
        "slurm_logs/04_delay_modeling/backside_delay_model_validate_20260228_1.model.tsv",
    ),
    (
        "validate_20260228_2_dualproxy",
        "slurm_logs/04_delay_modeling/backside_delay_model_validate_20260228_2_dualproxy.delay.tsv",
        "slurm_logs/04_delay_modeling/backside_delay_model_validate_20260228_2_dualproxy.model.tsv",
    ),
    (
        "validate_20260228_3_dualproxy_fused",
        "slurm_logs/04_delay_modeling/backside_delay_model_validate_20260228_3_dualproxy_fused.delay.tsv",
        "slurm_logs/04_delay_modeling/backside_delay_model_validate_20260228_3_dualproxy_fused.model.tsv",
    ),
]

BASE_FEATURES = [
    "hpwl_dbu",
    "pdk_timing_raw",
    "pdk_via_proxy_raw",
    "fanout_n",
]
PRESSURE_FEATURES = [
    "via_risk_n",
    "net_density_n",
    "fanout_n",
]


@dataclass
class GateCfg:
    min_delta_pearson: float
    min_delta_spearman: float
    min_delta_sign: float
    min_abs_pearson: float
    min_abs_spearman: float
    min_abs_sign: float
    min_win_pearson: float
    min_win_spearman: float
    min_win_sign: float
    require_capacity_effect: bool


def _safe_corr(x: np.ndarray, y: np.ndarray, kind: str) -> float:
    if len(x) < 3:
        return float("nan")
    if np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    if kind == "pearson":
        return float(pearsonr(x, y)[0])
    if kind == "spearman":
        return float(spearmanr(x, y)[0])
    raise ValueError(kind)


def _sign_acc(p: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean(np.sign(p) == np.sign(y)))


def _normalize_net(df: pd.DataFrame) -> pd.DataFrame:
    if "net" in df.columns:
        return df
    return df.rename(columns={df.columns[0]: "net"})


def _load_merged(delay_tsv: Path, model_tsv: Path) -> pd.DataFrame:
    d = _normalize_net(pd.read_csv(delay_tsv, sep="\t"))
    m = _normalize_net(pd.read_csv(model_tsv, sep="\t"))
    tgt = "delta_max_tau_ps" if "delta_max_tau_ps" in d.columns else "delta_tau_ps"
    cols = ["net", tgt] + [c for c in BASE_FEATURES + PRESSURE_FEATURES if c in m.columns]
    cols = list(dict.fromkeys(cols))
    dm = d[["net", tgt]].merge(m[[c for c in cols if c in m.columns]], on="net", how="inner")
    dm = dm.rename(columns={tgt: "target_delta_tau_ps"}).dropna()
    return dm


def _parse_dataset(raw: str) -> tuple[str, Path, Path]:
    x = raw.split(":", 2)
    if len(x) != 3:
        raise ValueError(f"bad dataset triple: {raw}")
    return x[0], Path(x[1]), Path(x[2])


def _pressure_proxy(df: pd.DataFrame) -> np.ndarray:
    v = df.get("via_risk_n", pd.Series(0.0, index=df.index)).astype(float).clip(lower=0)
    n = df.get("net_density_n", pd.Series(0.0, index=df.index)).astype(float).clip(lower=0)
    f = df.get("fanout_n", pd.Series(0.0, index=df.index)).astype(float).clip(lower=0)
    return (v * n * f).to_numpy()


def _select_lambda(
    pred_train: np.ndarray,
    y_train: np.ndarray,
    pressure_train: np.ndarray,
    lam_grid: np.ndarray,
) -> float:
    mu = float(np.mean(pressure_train))
    sd = float(np.std(pressure_train))
    if sd < 1e-12:
        return 0.0
    z = (pressure_train - mu) / sd
    best_lam = 0.0
    best_obj = -1e18
    for lam in lam_grid:
        pp = pred_train + lam * z
        pr = _safe_corr(pp, y_train, "pearson")
        sp = _safe_corr(pp, y_train, "spearman")
        sg = _sign_acc(pp, y_train)
        obj = (0.0 if np.isnan(sp) else sp) + 0.2 * (0.0 if np.isnan(pr) else pr) + 0.3 * sg
        if obj > best_obj:
            best_obj = obj
            best_lam = float(lam)
    return best_lam


def _dataset_pass(row: pd.Series, g: GateCfg) -> bool:
    delay_gate = all(
        [
            row["delta_pearson_mean"] > g.min_delta_pearson,
            row["delta_spearman_mean"] >= g.min_delta_spearman,
            row["delta_sign_mean"] > g.min_delta_sign,
            row["cand_pearson_mean"] >= g.min_abs_pearson,
            row["cand_spearman_mean"] >= g.min_abs_spearman,
            row["cand_sign_mean"] >= g.min_abs_sign,
            row["winrate_pearson"] >= g.min_win_pearson,
            row["winrate_spearman"] >= g.min_win_spearman,
            row["winrate_sign"] >= g.min_win_sign,
        ]
    )
    if not delay_gate:
        return False
    if not g.require_capacity_effect:
        return True
    return (row["lambda_mean"] > 0.0) and (row["topq_uplift_mean"] > 0.0)


def evaluate(
    datasets: Iterable[tuple[str, Path, Path]],
    splits: int,
    repeats: int,
    seed: int,
    cap_quantile: float,
    lam_grid: np.ndarray,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rkf = RepeatedKFold(n_splits=splits, n_repeats=repeats, random_state=seed)
    per_fold = []
    per_ds = []

    for ds_name, delay_path, model_path in datasets:
        df = _load_merged(delay_path, model_path)
        if df.empty or "hpwl_dbu" not in df.columns:
            per_ds.append({"dataset": ds_name, "status": "empty_or_missing_hpwl", "rows": len(df)})
            continue

        feats = [c for c in BASE_FEATURES if c in df.columns]
        X = df[feats].astype(float).to_numpy()
        Xhp = df[["hpwl_dbu"]].astype(float).to_numpy()
        y = df["target_delta_tau_ps"].astype(float).to_numpy()
        demand = _pressure_proxy(df)

        fold_rows = []
        f_id = 0
        for tr, te in rkf.split(X):
            f_id += 1
            xtr, xte = X[tr], X[te]
            xhtr, xhte = Xhp[tr], Xhp[te]
            ytr, yte = y[tr], y[te]
            dtr, dte = demand[tr], demand[te]

            hp = Ridge(alpha=1.0)
            hp.fit(xhtr, ytr)
            ph = hp.predict(xhte)

            base = RandomForestRegressor(
                n_estimators=300,
                max_depth=12,
                min_samples_leaf=2,
                n_jobs=-1,
                random_state=seed + f_id,
            )
            base.fit(xtr, ytr)
            pb_tr = base.predict(xtr)
            pb_te = base.predict(xte)

            cap_thr = float(np.quantile(dtr, cap_quantile))
            ptr = np.maximum(0.0, dtr - cap_thr)
            pte = np.maximum(0.0, dte - cap_thr)
            lam = _select_lambda(pb_tr, ytr, ptr, lam_grid)
            mu = float(np.mean(ptr))
            sd = float(np.std(ptr))
            if sd < 1e-12:
                zte = np.zeros_like(pte)
            else:
                zte = (pte - mu) / sd
            pa = pb_te + lam * zte

            top_thr = float(np.quantile(pte, 0.75)) if len(pte) else 0.0
            mask_top = pte >= top_thr
            if np.any(mask_top):
                uplift_top = float(np.mean((pa - pb_te)[mask_top]))
            else:
                uplift_top = 0.0

            row = {
                "dataset": ds_name,
                "fold": f_id,
                "rows_test": len(te),
                "cap_quantile": cap_quantile,
                "cap_thr_train": cap_thr,
                "lambda": lam,
                "topq_uplift": uplift_top,
                "hp_pearson": _safe_corr(ph, yte, "pearson"),
                "hp_spearman": _safe_corr(ph, yte, "spearman"),
                "hp_sign": _sign_acc(ph, yte),
                "cand_pearson": _safe_corr(pa, yte, "pearson"),
                "cand_spearman": _safe_corr(pa, yte, "spearman"),
                "cand_sign": _sign_acc(pa, yte),
            }
            row["delta_pearson"] = row["cand_pearson"] - row["hp_pearson"]
            row["delta_spearman"] = row["cand_spearman"] - row["hp_spearman"]
            row["delta_sign"] = row["cand_sign"] - row["hp_sign"]
            per_fold.append(row)
            fold_rows.append(row)

        fd = pd.DataFrame(fold_rows)
        per_ds.append(
            {
                "dataset": ds_name,
                "status": "ok",
                "rows": len(df),
                "features": ",".join(feats),
                "cap_quantile": cap_quantile,
                "hp_pearson_mean": fd["hp_pearson"].mean(),
                "hp_spearman_mean": fd["hp_spearman"].mean(),
                "hp_sign_mean": fd["hp_sign"].mean(),
                "cand_pearson_mean": fd["cand_pearson"].mean(),
                "cand_spearman_mean": fd["cand_spearman"].mean(),
                "cand_sign_mean": fd["cand_sign"].mean(),
                "delta_pearson_mean": fd["delta_pearson"].mean(),
                "delta_spearman_mean": fd["delta_spearman"].mean(),
                "delta_sign_mean": fd["delta_sign"].mean(),
                "winrate_pearson": float((fd["delta_pearson"] > 0).mean()),
                "winrate_spearman": float((fd["delta_spearman"] >= 0).mean()),
                "winrate_sign": float((fd["delta_sign"] > 0).mean()),
                "lambda_mean": fd["lambda"].mean(),
                "lambda_nonzero_frac": float((fd["lambda"] > 0).mean()),
                "topq_uplift_mean": fd["topq_uplift"].mean(),
            }
        )
    return pd.DataFrame(per_fold), pd.DataFrame(per_ds)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset", action="append", default=[], help="NAME:delay_tsv:model_tsv")
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--splits", type=int, default=5)
    ap.add_argument("--repeats", type=int, default=2)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--cap-quantile", type=float, default=0.75)
    ap.add_argument("--lambda-grid", default="0,0.005,0.01,0.02,0.03,0.05,0.08,0.1")
    ap.add_argument("--min-delta-pearson", type=float, default=0.0)
    ap.add_argument("--min-delta-spearman", type=float, default=0.0)
    ap.add_argument("--min-delta-sign", type=float, default=0.0)
    ap.add_argument("--min-abs-pearson", type=float, default=0.65)
    ap.add_argument("--min-abs-spearman", type=float, default=0.38)
    ap.add_argument("--min-abs-sign", type=float, default=0.62)
    ap.add_argument("--min-win-pearson", type=float, default=0.60)
    ap.add_argument("--min-win-spearman", type=float, default=0.55)
    ap.add_argument("--min-win-sign", type=float, default=0.60)
    ap.add_argument(
        "--require-capacity-effect",
        action="store_true",
        help="If set, each dataset must have lambda_mean>0 and topq_uplift_mean>0.",
    )
    args = ap.parse_args()

    lam_grid = np.array([float(x) for x in args.lambda_grid.split(",") if x.strip() != ""], dtype=float)
    if args.dataset:
        datasets = [_parse_dataset(x) for x in args.dataset]
    else:
        datasets = [(n, Path(d), Path(m)) for n, d, m in DEFAULT_DATASETS]

    cfg = GateCfg(
        min_delta_pearson=args.min_delta_pearson,
        min_delta_spearman=args.min_delta_spearman,
        min_delta_sign=args.min_delta_sign,
        min_abs_pearson=args.min_abs_pearson,
        min_abs_spearman=args.min_abs_spearman,
        min_abs_sign=args.min_abs_sign,
        min_win_pearson=args.min_win_pearson,
        min_win_spearman=args.min_win_spearman,
        min_win_sign=args.min_win_sign,
        require_capacity_effect=args.require_capacity_effect,
    )

    per_fold, per_ds = evaluate(
        datasets=datasets,
        splits=args.splits,
        repeats=args.repeats,
        seed=args.seed,
        cap_quantile=args.cap_quantile,
        lam_grid=lam_grid,
    )

    out_prefix = Path(args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    pf_tsv = out_prefix.with_suffix(".per_fold.tsv")
    ds_tsv = out_prefix.with_suffix(".dataset.tsv")
    md = out_prefix.with_suffix(".summary.md")
    per_fold.to_csv(pf_tsv, sep="\t", index=False)
    per_ds.to_csv(ds_tsv, sep="\t", index=False)

    ds_ok = per_ds[per_ds["status"] == "ok"].copy()
    if not ds_ok.empty:
        ds_ok["dataset_pass"] = ds_ok.apply(lambda r: _dataset_pass(r, cfg), axis=1)
        overall = bool(ds_ok["dataset_pass"].all())
    else:
        overall = False

    lines = []
    lines += [
        "# BS Cost Delay-Consistency + nTSV Capacity Gate",
        "",
        f"- out_prefix: `{out_prefix}`",
        f"- splits/repeats/seed: `{args.splits}/{args.repeats}/{args.seed}`",
        f"- cap_quantile: `{args.cap_quantile}`",
        f"- lambda_grid: `{args.lambda_grid}`",
        f"- require_capacity_effect: `{args.require_capacity_effect}`",
        "",
        "## Gate Thresholds",
        f"- delta vs HPWL: pearson>{cfg.min_delta_pearson}, spearman>={cfg.min_delta_spearman}, sign>{cfg.min_delta_sign}",
        f"- abs consistency: pearson>={cfg.min_abs_pearson}, spearman>={cfg.min_abs_spearman}, sign>={cfg.min_abs_sign}",
        f"- winrates: pearson>={cfg.min_win_pearson}, spearman>={cfg.min_win_spearman}, sign>={cfg.min_win_sign}",
        "",
        "## Dataset Results",
    ]
    if not per_ds.empty:
        show = per_ds.merge(ds_ok[["dataset", "dataset_pass"]], on="dataset", how="left")
        cols = [
            "dataset",
            "status",
            "rows",
            "cand_pearson_mean",
            "cand_spearman_mean",
            "cand_sign_mean",
            "delta_pearson_mean",
            "delta_spearman_mean",
            "delta_sign_mean",
            "lambda_mean",
            "lambda_nonzero_frac",
            "topq_uplift_mean",
            "dataset_pass",
        ]
        rep = show[[c for c in cols if c in show.columns]]
        try:
            lines.append(rep.to_markdown(index=False))
        except Exception:
            lines += ["```text", rep.to_string(index=False), "```"]
    lines += [
        "",
        "## Decision",
        f"- overall_pass: `{overall}`",
        "",
        "## Artifacts",
        f"- per_fold: `{pf_tsv}`",
        f"- dataset: `{ds_tsv}`",
        f"- summary: `{md}`",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote: {pf_tsv}")
    print(f"wrote: {ds_tsv}")
    print(f"wrote: {md}")
    print(f"overall_pass={overall}")
    return 0 if overall else 2


if __name__ == "__main__":
    raise SystemExit(main())

