#!/usr/bin/env python3
"""Experiment memory store for EDA runs (SQLite-backed)."""

import argparse
import csv
import datetime as dt
import hashlib
import json
import pathlib
import sqlite3
import sys
from typing import Dict, Iterable, List, Optional, Tuple


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


def is_success(status: str, result: str) -> int:
    su = (status or "").strip().upper()
    ru = (result or "").strip().upper()
    if su in {"FAIL", "FAILED", "CANCELLED", "TIMEOUT", "PRECHECK_FAIL"} or ru == "FAIL":
        return 0
    return 1 if (su in {"SUCCESS", "COMPLETED"} or ru == "PASS") else 0


def parse_design_from_run_dir(run_dir: str) -> str:
    p = pathlib.Path(run_dir or "")
    parts = p.parts
    for i, tok in enumerate(parts):
        if tok == "outputs" and i + 1 < len(parts):
            return parts[i + 1]
    return "NA"


def infer_phase(row: Dict[str, str]) -> str:
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
    if "cts" in mode:
        return "cts"
    return "other"


def infer_runtime_sec(row: Dict[str, str]) -> Optional[float]:
    for key in (
        "runtime_sec",
        "replace_runtime_sec",
        "select_runtime_sec",
        "eval_runtime_sec",
        "total_runtime_sec",
        "elapsed_sec",
    ):
        if key in row:
            v = to_float(row.get(key, ""))
            if v is not None:
                return v
    return None


def infer_metric(row: Dict[str, str], keys: Iterable[str]) -> Optional[float]:
    for k in keys:
        if k in row:
            v = to_float(row.get(k, ""))
            if v is not None:
                return v
    return None


EXCLUDE_PARAM_KEYS = {
    "design",
    "phase",
    "mode",
    "job_id",
    "dep",
    "status",
    "result",
    "run_dir",
    "stdout",
    "stderr",
    "wrapper",
    "manifest",
    "summary",
    "monitor",
    "hpwl_um",
    "hpwl",
    "area_um2",
    "area",
    "power_mw",
    "power",
    "wns_ns",
    "wns",
    "tns_ns",
    "tns",
    "viol_paths",
    "runtime_sec",
    "replace_runtime_sec",
    "select_runtime_sec",
    "eval_runtime_sec",
    "total_runtime_sec",
    "elapsed_sec",
    "source",
    "source_file",
    "source_kind",
    "source_run_tag",
}


def extract_param_dict(row: Dict[str, str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for k, v in row.items():
        key = (k or "").strip()
        if key == "":
            continue
        if key.lower() in EXCLUDE_PARAM_KEYS:
            continue
        val = "" if v is None else str(v).strip()
        if val == "" or val.upper() in {"NA", "N/A"}:
            continue
        if len(val) > 200:
            continue
        out[key] = val
    return out


def param_signature(param_dict: Dict[str, str]) -> str:
    if not param_dict:
        return ""
    keys = sorted(param_dict.keys())
    parts = ["{}={}".format(k, param_dict[k]) for k in keys]
    return "|".join(parts)


def row_hash(source_file: str, row_idx: int, row: Dict[str, str]) -> str:
    payload = {
        "source_file": source_file,
        "row_idx": row_idx,
        "row": row,
    }
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def default_db_path(root: pathlib.Path) -> pathlib.Path:
    return (root / DEFAULT_DB).resolve()


def open_db(db_path: pathlib.Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS experiment_rows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingest_ts TEXT NOT NULL,
            source_file TEXT NOT NULL,
            source_kind TEXT NOT NULL,
            source_run_tag TEXT NOT NULL,
            row_hash TEXT NOT NULL UNIQUE,
            design TEXT,
            phase TEXT,
            mode TEXT,
            job_id TEXT,
            status TEXT,
            result TEXT,
            success INTEGER,
            hpwl_um REAL,
            area_um2 REAL,
            power_mw REAL,
            wns_ns REAL,
            tns_ns REAL,
            runtime_sec REAL,
            selected_ratio_pct REAL,
            used_capacity_ratio_pct REAL,
            param_signature TEXT,
            param_json TEXT,
            raw_json TEXT NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_experiment_rows_main ON experiment_rows(design, phase, success)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_experiment_rows_source ON experiment_rows(source_run_tag, source_kind)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_experiment_rows_paramsig ON experiment_rows(param_signature)"
    )
    # Forward-compatible schema migration for older DB files.
    cur = conn.execute("PRAGMA table_info(experiment_rows)")
    cols = set(r[1] for r in cur.fetchall())
    if "param_signature" not in cols:
        conn.execute("ALTER TABLE experiment_rows ADD COLUMN param_signature TEXT")
    if "param_json" not in cols:
        conn.execute("ALTER TABLE experiment_rows ADD COLUMN param_json TEXT")
    conn.commit()


def detect_source_kind(path: pathlib.Path, row: Dict[str, str]) -> str:
    name = path.name.lower()
    if name.endswith(".run_manifest.tsv"):
        return "run_manifest"
    if "summary" in name:
        return "summary_tsv"
    if "monitor" in name:
        return "monitor_tsv"
    if "phase" in row or "job_id" in row:
        return "manifest_like"
    return "generic_tsv"


def detect_run_tag(path: pathlib.Path, row: Dict[str, str], override: str) -> str:
    if override:
        return override
    if "run_tag" in row and (row.get("run_tag") or "").strip():
        return (row.get("run_tag") or "").strip()
    stem = path.stem
    if stem.endswith(".run_manifest"):
        stem = stem[:-len(".run_manifest")]
    return stem


def ingest_file(conn: sqlite3.Connection, path: pathlib.Path, run_tag_override: str) -> Tuple[int, int]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        rd = csv.DictReader(f, delimiter="\t")
        rows = list(rd)

    inserted = 0
    skipped = 0
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i, row in enumerate(rows):
        run_dir = (row.get("run_dir") or "").strip()
        design = (row.get("design") or "").strip()
        if not design or design.upper() == "NA":
            design = parse_design_from_run_dir(run_dir)
        phase = infer_phase(row)
        mode = (row.get("mode") or "").strip() or "NA"
        status = (row.get("status") or "").strip() or "NA"
        result = (row.get("result") or "").strip() or "NA"
        job_id = (row.get("job_id") or "").strip() or "NA"

        hpwl = infer_metric(row, ("hpwl_um", "hpwl", "total_hpwl_um", "total_hpwl_dbu"))
        area = infer_metric(row, ("area_um2", "area"))
        power = infer_metric(row, ("power_mw", "power"))
        wns = infer_metric(row, ("wns_ns", "wns"))
        tns = infer_metric(row, ("tns_ns", "tns"))
        runtime = infer_runtime_sec(row)
        sel_ratio = infer_metric(row, ("selected_ratio_pct",))
        used_ratio = infer_metric(row, ("used_capacity_ratio_pct",))

        source_kind = detect_source_kind(path, row)
        source_run_tag = detect_run_tag(path, row, run_tag_override)
        rh = row_hash(str(path), i, row)
        pmap = extract_param_dict(row)
        psig = param_signature(pmap)

        try:
            succ = is_success(status, result)
            if succ == 0:
                # For partially backfilled tables, status/result may be NA while metrics exist.
                if any(x is not None for x in (hpwl, area, power, wns, tns)):
                    succ = 1

            conn.execute(
                """
                INSERT INTO experiment_rows(
                    ingest_ts, source_file, source_kind, source_run_tag, row_hash,
                    design, phase, mode, job_id, status, result, success,
                    hpwl_um, area_um2, power_mw, wns_ns, tns_ns, runtime_sec,
                    selected_ratio_pct, used_capacity_ratio_pct, param_signature, param_json, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now,
                    str(path),
                    source_kind,
                    source_run_tag,
                    rh,
                    design,
                    phase,
                    mode,
                    job_id,
                    status,
                    result,
                    succ,
                    hpwl,
                    area,
                    power,
                    wns,
                    tns,
                    runtime,
                    sel_ratio,
                    used_ratio,
                    psig,
                    json.dumps(pmap, ensure_ascii=True, sort_keys=True),
                    json.dumps(row, ensure_ascii=True, sort_keys=True),
                ),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1
    conn.commit()
    return inserted, skipped


def query_rows(
    conn: sqlite3.Connection,
    design: str,
    phase: str,
    limit: int,
    only_success: bool,
    metric: str,
    direction: str,
    wns_min: Optional[float],
) -> List[tuple]:
    order = "ASC" if direction == "min" else "DESC"
    sql = (
        "SELECT source_run_tag, design, phase, mode, job_id, status, result, success, "
        "hpwl_um, area_um2, power_mw, wns_ns, tns_ns, runtime_sec, selected_ratio_pct, used_capacity_ratio_pct "
        "FROM experiment_rows WHERE 1=1"
    )
    args: List[object] = []
    if design:
        sql += " AND design=?"
        args.append(design)
    if phase:
        sql += " AND phase=?"
        args.append(phase)
    if only_success:
        sql += " AND success=1"
    if wns_min is not None:
        sql += " AND wns_ns IS NOT NULL AND wns_ns>=?"
        args.append(wns_min)
    sql += " ORDER BY CASE WHEN {m} IS NULL THEN 1 ELSE 0 END, {m} {o} LIMIT ?".format(m=metric, o=order)
    args.append(limit)
    cur = conn.execute(sql, args)
    return list(cur.fetchall())


def cmd_init(args: argparse.Namespace) -> int:
    db = pathlib.Path(args.db).resolve()
    conn = open_db(db)
    init_schema(conn)
    conn.close()
    print("db={}".format(db))
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    db = pathlib.Path(args.db).resolve()
    conn = open_db(db)
    init_schema(conn)
    total_inserted = 0
    total_skipped = 0
    for src in args.inputs:
        p = pathlib.Path(src).resolve()
        if not p.is_file():
            print("WARN: skip missing input {}".format(p))
            continue
        ins, sk = ingest_file(conn, p, args.run_tag)
        total_inserted += ins
        total_skipped += sk
        print("ingest {} inserted={} skipped={}".format(p, ins, sk))
    conn.close()
    print("total_inserted={}".format(total_inserted))
    print("total_skipped={}".format(total_skipped))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    db = pathlib.Path(args.db).resolve()
    if not db.is_file():
        print("ERROR: db not found {}".format(db), file=sys.stderr)
        return 2
    conn = open_db(db)
    rows = query_rows(
        conn=conn,
        design=args.design,
        phase=args.phase,
        limit=args.limit,
        only_success=bool(args.only_success),
        metric=args.metric,
        direction=args.direction,
        wns_min=args.wns_min,
    )
    conn.close()

    headers = [
        "run_tag",
        "design",
        "phase",
        "mode",
        "job_id",
        "status",
        "result",
        "success",
        "hpwl_um",
        "area_um2",
        "power_mw",
        "wns_ns",
        "tns_ns",
        "runtime_sec",
        "selected_ratio_pct",
        "used_capacity_ratio_pct",
    ]
    if args.out_tsv:
        out = pathlib.Path(args.out_tsv).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8", newline="") as f:
            wr = csv.writer(f, delimiter="\t")
            wr.writerow(headers)
            wr.writerows(rows)
        print("out_tsv={}".format(out))

    print("\t".join(headers))
    for r in rows:
        print("\t".join("" if v is None else str(v) for v in r))
    print("rows={}".format(len(rows)))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    db = pathlib.Path(args.db).resolve()
    if not db.is_file():
        print("ERROR: db not found {}".format(db), file=sys.stderr)
        return 2
    conn = open_db(db)
    cur = conn.execute(
        """
        SELECT design, phase,
               COUNT(*) AS n_rows,
               SUM(success) AS n_success,
               MIN(power_mw) AS best_power_mw,
               MIN(hpwl_um) AS best_hpwl_um,
               MAX(wns_ns) AS best_wns_ns
        FROM experiment_rows
        GROUP BY design, phase
        ORDER BY design, phase
        """
    )
    rows = list(cur.fetchall())
    conn.close()

    out_md = pathlib.Path(args.out_md).resolve()
    out_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Experiment Memory Report",
        "",
        "- db: `{}`".format(db),
        "- rows: `{}`".format(sum(r[2] for r in rows)),
        "",
        "| design | phase | rows | success | best_power_mW(min) | best_hpwl_um(min) | best_wns_ns(max) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        design, phase, n_rows, n_success, best_power, best_hpwl, best_wns = r
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} |".format(
                design,
                phase,
                n_rows,
                n_success if n_success is not None else 0,
                "NA" if best_power is None else "{:.6g}".format(best_power),
                "NA" if best_hpwl is None else "{:.6g}".format(best_hpwl),
                "NA" if best_wns is None else "{:.6g}".format(best_wns),
            )
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("out_md={}".format(out_md))
    return 0


def build_parser(root: pathlib.Path) -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Experiment memory store and query utility")
    sub = ap.add_subparsers(dest="cmd")

    p_init = sub.add_parser("init", help="Initialize experiment memory DB")
    p_init.add_argument("--db", default=str(default_db_path(root)))
    p_init.set_defaults(func=cmd_init)

    p_ing = sub.add_parser("ingest", help="Ingest manifest/tsv files into memory DB")
    p_ing.add_argument("inputs", nargs="+", help="Input TSV files")
    p_ing.add_argument("--db", default=str(default_db_path(root)))
    p_ing.add_argument("--run-tag", default="", help="Override source run tag")
    p_ing.set_defaults(func=cmd_ingest)

    p_q = sub.add_parser("query", help="Query best rows with constraints")
    p_q.add_argument("--db", default=str(default_db_path(root)))
    p_q.add_argument("--design", default="")
    p_q.add_argument("--phase", default="")
    p_q.add_argument("--limit", type=int, default=20)
    p_q.add_argument("--only-success", type=int, default=1)
    p_q.add_argument(
        "--metric",
        default="power_mw",
        choices=[
            "power_mw",
            "hpwl_um",
            "area_um2",
            "wns_ns",
            "tns_ns",
            "runtime_sec",
            "selected_ratio_pct",
            "used_capacity_ratio_pct",
        ],
    )
    p_q.add_argument("--direction", default="min", choices=["min", "max"])
    p_q.add_argument("--wns-min", type=float, default=None)
    p_q.add_argument("--out-tsv", default="")
    p_q.set_defaults(func=cmd_query)

    p_r = sub.add_parser("report", help="Generate markdown report from DB")
    p_r.add_argument("--db", default=str(default_db_path(root)))
    p_r.add_argument(
        "--out-md",
        default=str(root / "slurm_logs/04_delay_modeling/experiment_memory_report.md"),
    )
    p_r.set_defaults(func=cmd_report)

    return ap


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[2]
    ap = build_parser(root)
    args = ap.parse_args()
    if not hasattr(args, "func"):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
