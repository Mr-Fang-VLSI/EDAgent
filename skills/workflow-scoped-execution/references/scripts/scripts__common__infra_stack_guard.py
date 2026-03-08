#!/usr/bin/env python3
"""Audit core infrastructure integrity: AGENTS policy, KB, tool registry, and skills."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass
class CheckRow:
    scope: str
    item: str
    level: str
    status: str
    detail: str


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Infrastructure stack guard for EDA repo")
    ap.add_argument(
        "--out-prefix",
        default="slurm_logs/00_meta/infra_stack_guard_latest",
        help="output prefix for markdown/tsv artifacts",
    )
    return ap.parse_args()


def parse_calls(s: str) -> List[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def read_manifest(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def check_file(rows: List[CheckRow], scope: str, rel: str, level: str = "critical") -> None:
    p = ROOT / rel
    if p.is_file():
        rows.append(CheckRow(scope, rel, level, "PASS", "file exists"))
    else:
        rows.append(CheckRow(scope, rel, level, "FAIL", "missing required file"))


def run_checks() -> List[CheckRow]:
    rows: List[CheckRow] = []

    # AGENTS policy baseline
    check_file(rows, "agent_policy", "AGENTS.md")

    # Knowledge base baseline
    for rel in [
        "docs/knowledge_base/README.md",
        "docs/knowledge_base/00_START_HERE.md",
        "docs/knowledge_base/10_TASK_EXECUTION_PROTOCOL.md",
        "docs/knowledge_base/11_INTERACTION_CHECKLIST.md",
        "docs/knowledge_base/90_HYPOTHESIS_VALIDATION_LOG.md",
        "docs/knowledge_base/93_EDA_RESEARCH_FULL_CHAIN_20260306.md",
    ]:
        check_file(rows, "knowledge_base", rel)

    # Tool registry baseline
    for rel in [
        "docs/tool_registry/README.md",
        "docs/tool_registry/tool_catalog.tsv",
        "docs/tool_registry/tool_catalog.md",
        "docs/tool_registry/tool_metadata.tsv",
        "scripts/common/tool_catalog.py",
        "scripts/common/unified_kb_query.py",
    ]:
        check_file(rows, "tool_registry", rel)

    # Skill system baseline
    manifest_rel = "skills/00_SKILL_SYSTEM_MANIFEST.tsv"
    check_file(rows, "skill_system", manifest_rel)
    manifest_path = ROOT / manifest_rel
    if manifest_path.is_file():
        skills = read_manifest(manifest_path)
        known = {r["skill"] for r in skills}
        for r in skills:
            skill_name = r["skill"]
            base = ROOT / "skills" / skill_name
            if (base / "SKILL.md").is_file():
                rows.append(CheckRow("skill_system", f"skills/{skill_name}/SKILL.md", "critical", "PASS", "skill body exists"))
            else:
                rows.append(CheckRow("skill_system", f"skills/{skill_name}/SKILL.md", "critical", "FAIL", "missing skill body"))

            if (base / "agents" / "openai.yaml").is_file():
                rows.append(
                    CheckRow("skill_system", f"skills/{skill_name}/agents/openai.yaml", "warning", "PASS", "ui metadata exists")
                )
            else:
                rows.append(
                    CheckRow("skill_system", f"skills/{skill_name}/agents/openai.yaml", "warning", "WARN", "ui metadata missing")
                )

            for callee in parse_calls(r.get("calls", "")):
                if callee not in known:
                    rows.append(
                        CheckRow(
                            "skill_system",
                            f"{skill_name} -> {callee}",
                            "critical",
                            "FAIL",
                            "manifest dependency target missing",
                        )
                    )
                else:
                    rows.append(
                        CheckRow(
                            "skill_system",
                            f"{skill_name} -> {callee}",
                            "info",
                            "PASS",
                            "dependency target exists",
                        )
                    )

    # Guard scripts baseline
    for rel in [
        "scripts/common/knowledge_gate.sh",
        "scripts/common/skill_system_audit.py",
        "scripts/common/infra_stack_guard.py",
        "scripts/common/init_research_chain.py",
        "scripts/common/research_chain_guard.py",
    ]:
        check_file(rows, "guard_stack", rel)

    return rows


def write_tsv(path: Path, rows: List[CheckRow]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["scope", "item", "level", "status", "detail"])
        for r in rows:
            w.writerow([r.scope, r.item, r.level, r.status, r.detail])


def write_summary(path: Path, rows: List[CheckRow], tsv_path: Path) -> None:
    crit_fail = [r for r in rows if r.level == "critical" and r.status == "FAIL"]
    warn_rows = [r for r in rows if r.status == "WARN"]
    status = "PASS" if not crit_fail else "FAIL"

    by_scope: Dict[str, List[CheckRow]] = {}
    for r in rows:
        by_scope.setdefault(r.scope, []).append(r)

    lines: List[str] = []
    lines.append("# Infra Stack Guard Summary")
    lines.append("")
    lines.append(f"- timestamp: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append(f"- root: `{ROOT}`")
    lines.append(f"- overall_status: `{status}`")
    lines.append(f"- critical_fail_count: `{len(crit_fail)}`")
    lines.append(f"- warning_count: `{len(warn_rows)}`")
    lines.append("")
    lines.append("## Scope Scoreboard")
    lines.append("| scope | pass | warn | fail |")
    lines.append("|---|---:|---:|---:|")
    for scope in sorted(by_scope.keys()):
        ps = sum(1 for r in by_scope[scope] if r.status == "PASS")
        ws = sum(1 for r in by_scope[scope] if r.status == "WARN")
        fs = sum(1 for r in by_scope[scope] if r.status == "FAIL")
        lines.append(f"| {scope} | {ps} | {ws} | {fs} |")
    lines.append("")

    if crit_fail:
        lines.append("## Critical Fails")
        for r in crit_fail[:50]:
            lines.append(f"- `{r.scope}` `{r.item}`: {r.detail}")
        lines.append("")
    else:
        lines.append("## Critical Fails")
        lines.append("- none")
        lines.append("")

    if warn_rows:
        lines.append("## Warnings")
        for r in warn_rows[:50]:
            lines.append(f"- `{r.scope}` `{r.item}`: {r.detail}")
        lines.append("")
    else:
        lines.append("## Warnings")
        lines.append("- none")
        lines.append("")

    lines.append("## Artifacts")
    lines.append(f"- detail_tsv: `{tsv_path}`")
    lines.append(f"- summary_md: `{path}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    out_prefix = Path(args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    rows = run_checks()

    out_tsv = out_prefix.with_suffix(".detail.tsv")
    out_md = out_prefix.with_suffix(".summary.md")
    write_tsv(out_tsv, rows)
    write_summary(out_md, rows, out_tsv)

    crit_fail = [r for r in rows if r.level == "critical" and r.status == "FAIL"]
    print(f"wrote: {out_tsv}")
    print(f"wrote: {out_md}")
    print(f"overall_status={'PASS' if not crit_fail else 'FAIL'}")
    return 0 if not crit_fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
