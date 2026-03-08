#!/usr/bin/env python3
"""Report conda roots, environments, and selected package availability for this project.

The goal is not full environment provisioning. The goal is to give the repo a
stable, scriptable snapshot of which conda installations and envs are usable
for project workflows, plus whether key analysis/runtime packages are present.
"""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Set


DEFAULT_ROOTS = [
    Path.home() / "miniconda3",
    Path("/mnt/research/Hu_Jiang/Students/Fang_Donghao/anaconda3"),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-prefix", required=True, help="Output prefix for report artifacts.")
    p.add_argument(
        "--env",
        action="append",
        default=[],
        help="Explicit env name to inspect. Repeatable. If omitted, inspect all discovered envs.",
    )
    p.add_argument(
        "--package",
        action="append",
        default=["numpy", "pandas", "scikit-learn"],
        help="Package/module name to probe inside each env. Repeatable.",
    )
    p.add_argument(
        "--probe-timeout-sec",
        type=int,
        default=20,
        help="Timeout for one `conda run` package probe.",
    )
    return p.parse_args()


def discover_conda_bins() -> List[Path]:
    found = []  # type: List[Path]
    seen = set()  # type: Set[str]
    for root in DEFAULT_ROOTS:
        cand = root / "bin" / "conda"
        if cand.exists():
            resolved = str(cand.resolve())
            if resolved not in seen:
                found.append(cand)
                seen.add(resolved)
    path_conda = shutil.which("conda")
    if path_conda:
        resolved = str(Path(path_conda).resolve())
        if resolved not in seen:
            found.append(Path(path_conda))
            seen.add(resolved)
    return found


def run_json(cmd: List[str]) -> Dict[str, object]:
    res = subprocess.run(
        cmd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if res.returncode != 0:
        return {"_error": res.stderr.strip() or res.stdout.strip(), "_cmd": " ".join(cmd)}
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return {"_error": "invalid_json", "_cmd": " ".join(cmd), "_stdout": res.stdout[:1000]}


def probe_env(conda_bin: Path, env_name: str, packages: List[str], timeout_sec: int) -> Dict[str, object]:
    code = [
        "import importlib.util",
        "mods = " + repr(packages),
        "out = {}",
        "for m in mods:",
        "    out[m] = 1 if importlib.util.find_spec(m.replace('-', '_')) is not None else 0",
        "print(__import__('json').dumps(out, sort_keys=True))",
    ]
    try:
        res = subprocess.run(
            [str(conda_bin), "run", "-n", env_name, "python", "-c", "; ".join(code)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired:
        return {"status": "probe_timeout", "detail": f"timeout>{timeout_sec}s"}
    if res.returncode != 0:
        return {"status": "probe_failed", "detail": res.stderr.strip() or res.stdout.strip()}
    try:
        data = json.loads(res.stdout.strip())
        return {"status": "ok", **data}
    except json.JSONDecodeError:
        return {"status": "probe_failed", "detail": "invalid_probe_json"}


def main() -> int:
    args = parse_args()
    conda_bins = discover_conda_bins()
    out_prefix = Path(args.out_prefix)
    if not out_prefix.is_absolute():
        out_prefix = (Path.cwd() / out_prefix).resolve()
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    report_tsv = Path(str(out_prefix) + ".envs.tsv")
    summary_md = Path(str(out_prefix) + ".summary.md")

    rows = []  # type: List[Dict[str, str]]
    total_envs = 0
    for conda_bin in conda_bins:
        info = run_json([str(conda_bin), "info", "--envs", "--json"])
        envs = info.get("envs", []) if isinstance(info, dict) else []
        env_names = []
        for env_path in envs:
            env_path = Path(env_path)
            env_name = env_path.name
            if args.env and env_name not in args.env:
                continue
            env_names.append((env_name, env_path))
        for env_name, env_path in env_names:
            total_envs += 1
            probe = probe_env(conda_bin, env_name, args.package, args.probe_timeout_sec)
            row = {
                "conda_bin": str(conda_bin),
                "env_name": env_name,
                "env_path": str(env_path),
                "probe_status": probe.get("status", "unknown"),
            }
            for pkg in args.package:
                key = pkg.replace("-", "_")
                row[f"has_{key}"] = str(probe.get(pkg, probe.get(key, 0)))
            row["probe_detail"] = probe.get("detail", "")
            rows.append(row)

    fields = ["conda_bin", "env_name", "env_path", "probe_status"] + [f"has_{p.replace('-', '_')}" for p in args.package] + ["probe_detail"]
    with report_tsv.open("w", encoding="utf-8", newline="") as f:
        import csv

        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        for row in rows:
            w.writerow(row)

    usable = sum(1 for row in rows if row["probe_status"] == "ok")
    lines = [
        "# Conda Project Environment Report",
        "",
        f"- discovered_conda_bins: `{len(conda_bins)}`",
        f"- inspected_envs: `{total_envs}`",
        f"- probe_ok_envs: `{usable}`",
        f"- report_tsv: `{report_tsv}`",
        "",
        "## Conda Bins",
    ]
    for conda_bin in conda_bins:
        lines.append(f"- `{conda_bin}`")
    lines.extend(["", "## Notes", "- This report is a snapshot for project environment management, not a full lockfile.", "- Use explicit `conda run -n <env>` in project scripts when reproducibility matters.", ""])
    summary_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"report_tsv={report_tsv}")
    print(f"summary_md={summary_md}")
    print(f"inspected_envs={total_envs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
