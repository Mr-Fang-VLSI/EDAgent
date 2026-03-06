#!/usr/bin/env python3
"""Enforce theory-veto decision before expensive submissions."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", required=True, help="path to theory veto markdown report")
    ap.add_argument("--allow-conditional", type=int, default=1, help="1 allows CONDITIONAL, 0 blocks it")
    ap.add_argument("--override", type=int, default=0, help="1 bypasses NO-GO (must be explicit)")
    return ap.parse_args()


def read_verdict(report: Path) -> str:
    txt = report.read_text(encoding="utf-8", errors="ignore")
    for ln in txt.splitlines():
        s = ln.strip().upper()
        if s.startswith("- `GO`"):
            return "GO"
        if s.startswith("- `CONDITIONAL`"):
            return "CONDITIONAL"
        if s.startswith("- `NO-GO`"):
            return "NO-GO"
        if "VERDICT:" in s:
            if "NO-GO" in s:
                return "NO-GO"
            if "CONDITIONAL" in s:
                return "CONDITIONAL"
            if "GO" in s:
                return "GO"
    raise RuntimeError(f"cannot_parse_verdict_from_report: {report}")


def main() -> int:
    args = parse_args()
    report = Path(args.report)
    if not report.is_file():
        print(f"theory_veto_gate=FAIL missing_report={report}")
        return 2

    verdict = read_verdict(report)
    allow_conditional = int(args.allow_conditional) == 1
    override = int(args.override) == 1

    if verdict == "NO-GO":
        if override:
            print(f"theory_veto_gate=OVERRIDDEN verdict={verdict} report={report}")
            return 0
        print(f"theory_veto_gate=BLOCK verdict={verdict} report={report}")
        return 3

    if verdict == "CONDITIONAL" and not allow_conditional:
        print(f"theory_veto_gate=BLOCK verdict={verdict} report={report}")
        return 4

    print(f"theory_veto_gate=PASS verdict={verdict} report={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

