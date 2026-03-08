#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Audit local skill system: entry policy, overlap, dependency, and gap hints.")
    ap.add_argument(
        "--manifest",
        default="skills/00_SKILL_SYSTEM_MANIFEST.tsv",
        help="TSV manifest for skill system",
    )
    ap.add_argument(
        "--out-prefix",
        default="slurm_logs/00_meta/skill_system_audit_latest",
        help="output prefix for markdown/tsv",
    )
    return ap.parse_args()


def read_manifest(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def parse_tags(s: str) -> List[str]:
    return [x.strip() for x in (s or "").split(";") if x.strip()]


def parse_calls(s: str) -> List[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def parse_tool_deps(s: str) -> List[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def is_semver(v: str) -> bool:
    return bool(re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", (v or "").strip()))


def read_tool_ids(tool_catalog_path: Path) -> set:
    if not tool_catalog_path.exists():
        return set()
    with tool_catalog_path.open("r", encoding="utf-8", errors="ignore") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    return {r.get("tool_id", "").strip() for r in rows if r.get("tool_id", "").strip()}


def file_exists_for_skill(root: Path, skill: str) -> Dict[str, bool]:
    d = root / skill
    return {
        "skill_md": (d / "SKILL.md").exists(),
        "openai_yaml": (d / "agents" / "openai.yaml").exists(),
        "refs_dir": (d / "references").exists(),
    }


def reference_stats_for_skill(root: Path, skill: str) -> Tuple[int, int]:
    refs_dir = root / skill / "references"
    if not refs_dir.exists():
        return 0, 0
    ref_files = sorted(refs_dir.glob("*.md"))
    long_ref_count = 0
    for path in ref_files:
        try:
            line_count = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore"))
        except OSError:
            line_count = 0
        if line_count > 200:
            long_ref_count += 1
    return len(ref_files), long_ref_count


def skill_md_line_count(root: Path, skill: str) -> int:
    skill_md = root / skill / "SKILL.md"
    if not skill_md.exists():
        return 0
    try:
        return sum(1 for _ in skill_md.open("r", encoding="utf-8", errors="ignore"))
    except OSError:
        return 0


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest)
    out_prefix = Path(args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    rows = read_manifest(manifest_path)

    skills_root = manifest_path.parent
    repo_root = manifest_path.parent.parent
    tool_catalog_path = repo_root / "docs" / "tool_registry" / "tool_catalog.tsv"
    known_tool_ids = read_tool_ids(tool_catalog_path)
    required_cols = {
        "skill",
        "layer",
        "user_entry",
        "status",
        "skill_version",
        "interface_version",
        "scope_tags",
        "calls",
        "depends_on_tools",
        "kb_touch",
        "tool_touch",
        "gate_touch",
        "notes",
    }
    missing_cols = sorted(required_cols - set(rows[0].keys())) if rows else sorted(required_cols)
    if missing_cols:
        print(f"ERROR: manifest missing required columns: {','.join(missing_cols)}")
        return 2

    known = {r["skill"] for r in rows}

    # Agent/entry policy
    agent_md_path = repo_root / "AGENTS.md"
    agent_md_exists = agent_md_path.exists()
    entry_skills = [r["skill"] for r in rows if r.get("user_entry", "0").strip() == "1" and r.get("status", "") == "active"]
    entry_count_ok = len(entry_skills) <= 1
    entry_name_ok = True
    entry_policy_ok = agent_md_exists and entry_count_ok and entry_name_ok

    # Dependency checks
    missing_calls: List[str] = []
    for r in rows:
        for callee in parse_calls(r.get("calls", "")):
            if callee not in known:
                missing_calls.append(f"{r['skill']} -> {callee}")

    # Version and tool dependency checks
    bad_versions: List[str] = []
    missing_tool_deps: List[str] = []
    external_tool_allowlist = {"git", "python3", "bash", "node"}
    non_toolid_format: List[str] = []
    for r in rows:
        if not is_semver(r.get("skill_version", "")):
            bad_versions.append(f"{r['skill']} skill_version={r.get('skill_version', '')}")
        if not is_semver(r.get("interface_version", "")):
            bad_versions.append(f"{r['skill']} interface_version={r.get('interface_version', '')}")
        for dep in parse_tool_deps(r.get("depends_on_tools", "")):
            if dep in external_tool_allowlist:
                continue
            if "/" in dep:
                non_toolid_format.append(f"{r['skill']} -> {dep}")
                continue
            if dep not in known_tool_ids:
                missing_tool_deps.append(f"{r['skill']} -> {dep}")

    # Coverage checks
    fs_rows: List[Dict[str, str]] = []
    ref_rows: List[Dict[str, str]] = []
    for r in rows:
        chk = file_exists_for_skill(skills_root, r["skill"])
        ref_count, long_ref_count = reference_stats_for_skill(skills_root, r["skill"])
        skill_lines = skill_md_line_count(skills_root, r["skill"])
        fs_rows.append(
            {
                "skill": r["skill"],
                "has_skill_md": "yes" if chk["skill_md"] else "no",
                "has_openai_yaml": "yes" if chk["openai_yaml"] else "no",
                "has_references_dir": "yes" if chk["refs_dir"] else "no",
            }
        )
        ref_rows.append(
            {
                "skill": r["skill"],
                "ref_md_count": str(ref_count),
                "long_ref_count_gt_200_lines": str(long_ref_count),
                "ref_count_status": "FAIL" if ref_count > 10 else "PASS",
                "single_case_risk": "WARN" if long_ref_count > 0 else "OK",
            }
        )
        heavy_skill_entry_risk = "WARN" if skill_lines > 80 and ref_count < 2 else "OK"
        ref_rows[-1]["skill_md_lines"] = str(skill_lines)
        ref_rows[-1]["heavy_skill_entry_risk"] = heavy_skill_entry_risk

    # Overlap detection: tags appearing in multiple active skills.
    tag_map: Dict[str, List[str]] = defaultdict(list)
    for r in rows:
        if r.get("status") != "active":
            continue
        for t in parse_tags(r.get("scope_tags", "")):
            tag_map[t].append(r["skill"])
    overlap_rows: List[Dict[str, str]] = []
    for t, lst in sorted(tag_map.items()):
        if len(lst) > 1:
            overlap_rows.append({"scope_tag": t, "skills": ",".join(sorted(lst)), "count": str(len(lst))})

    # Gap hints
    all_tags = set(tag_map.keys())
    gap_hints: List[Dict[str, str]] = []
    if "portfolio_planning" not in all_tags:
        gap_hints.append(
            {
                "gap": "portfolio_planning",
                "suggested_skill": "eda-portfolio-manager",
                "priority": "high",
                "reason": "No skill explicitly manages multi-batch prioritization/resource budgeting.",
            }
        )
    if "result_warehouse" not in all_tags:
        gap_hints.append(
            {
                "gap": "result_warehouse",
                "suggested_skill": "eda-results-regression",
                "priority": "high",
                "reason": "No dedicated skill for normalized experiment database/golden regression snapshots.",
            }
        )
    if "visual_insight" not in all_tags:
        gap_hints.append(
            {
                "gap": "visual_insight",
                "suggested_skill": "eda-viz-insight",
                "priority": "medium",
                "reason": "No dedicated skill for standardized visual diagnostics and publication-ready plots.",
            }
        )
    if "infra_governance" not in all_tags:
        gap_hints.append(
            {
                "gap": "infra_governance",
                "suggested_skill": "eda-infra-maintainer",
                "priority": "high",
                "reason": "No dedicated skill owns lifecycle maintenance for agent/knowledge/tool/skill infrastructure.",
            }
        )
    if "knowledge_exploration" not in all_tags:
        gap_hints.append(
            {
                "gap": "knowledge_exploration",
                "suggested_skill": "control-knowledge-explorer",
                "priority": "high",
                "reason": "No dedicated skill maps knowledge/evidence gaps before literature and experiment planning.",
            }
        )
    if "idea_brainstorm" not in all_tags:
        gap_hints.append(
            {
                "gap": "idea_brainstorm",
                "suggested_skill": "eda-idea-debate-lab",
                "priority": "medium",
                "reason": "No dedicated skill performs structured brainstorming and adversarial idea refinement.",
            }
        )
    if "hypothesis_design" not in all_tags:
        gap_hints.append(
            {
                "gap": "hypothesis_design",
                "suggested_skill": "eda-hypothesis-experiment-designer",
                "priority": "high",
                "reason": "No dedicated skill converts ideas into falsifiable hypothesis/experiment matrices.",
            }
        )
    if "method_implementation" not in all_tags:
        gap_hints.append(
            {
                "gap": "method_implementation",
                "suggested_skill": "eda-method-implementer",
                "priority": "high",
                "reason": "No dedicated skill governs implementation from approved hypotheses with integration contract.",
            }
        )
    if "research_chain" not in all_tags:
        gap_hints.append(
            {
                "gap": "research_chain",
                "suggested_skill": "workflow-research-chain",
                "priority": "high",
                "reason": "No end-to-end workflow skill coordinates knowledge-to-validation chain.",
            }
        )
    if "bspdn_goal_tracking" not in all_tags:
        gap_hints.append(
            {
                "gap": "bspdn_goal_tracking",
                "suggested_skill": "bspdn-goal-driver",
                "priority": "high",
                "reason": "No dedicated skill tracks and gates progress toward explicit BSPDN power/timing targets.",
            }
        )

    # Emit TSV artifact for overlaps + gaps.
    out_overlap = out_prefix.with_suffix(".overlap.tsv")
    out_gap = out_prefix.with_suffix(".gaps.tsv")
    out_fs = out_prefix.with_suffix(".fscheck.tsv")
    out_ref = out_prefix.with_suffix(".refcheck.tsv")
    out_md = out_prefix.with_suffix(".summary.md")

    with out_overlap.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["scope_tag", "skills", "count"], delimiter="\t")
        w.writeheader()
        for r in overlap_rows:
            w.writerow(r)

    with out_gap.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["gap", "suggested_skill", "priority", "reason"], delimiter="\t")
        w.writeheader()
        for r in gap_hints:
            w.writerow(r)

    with out_fs.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["skill", "has_skill_md", "has_openai_yaml", "has_references_dir"], delimiter="\t")
        w.writeheader()
        for r in fs_rows:
            w.writerow(r)

    with out_ref.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "skill",
                "ref_md_count",
                "long_ref_count_gt_200_lines",
                "ref_count_status",
                "single_case_risk",
                "skill_md_lines",
                "heavy_skill_entry_risk",
            ],
            delimiter="\t",
        )
        w.writeheader()
        for r in ref_rows:
            w.writerow(r)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: List[str] = []
    lines.append("# Skill System Audit")
    lines.append("")
    lines.append(f"- timestamp: `{ts}`")
    lines.append(f"- manifest: `{manifest_path}`")
    lines.append(f"- agent_md: `{agent_md_path}`")
    lines.append(f"- agent_md_exists: `{'YES' if agent_md_exists else 'NO'}`")
    lines.append(f"- active_entry_skills: `{','.join(entry_skills) if entry_skills else 'none'}`")
    lines.append("- entry_policy_rule: `AGENTS.md must exist; active entry skills <=1; no compatibility entry skill is required`")
    lines.append(f"- entry_policy_ok: `{'YES' if entry_policy_ok else 'NO'}`")
    lines.append("")
    lines.append("## Dependency Check")
    if missing_calls:
        lines.append("- status: `FAIL`")
        lines.append("```text")
        for m in missing_calls:
            lines.append(m)
        lines.append("```")
    else:
        lines.append("- status: `PASS`")
    lines.append("")
    lines.append("## Version Contract Check")
    if bad_versions:
        lines.append("- status: `FAIL`")
        lines.append("```text")
        for v in bad_versions:
            lines.append(v)
        lines.append("```")
    else:
        lines.append("- status: `PASS`")
    lines.append("")

    lines.append("## Tool Dependency Path Check")
    lines.append(f"- tool_catalog: `{tool_catalog_path}`")
    lines.append(f"- known_tool_id_count: `{len(known_tool_ids)}`")
    if missing_tool_deps:
        lines.append("- status: `FAIL`")
        lines.append("```text")
        for m in missing_tool_deps:
            lines.append(m)
        lines.append("```")
    else:
        lines.append("- status: `PASS`")
    lines.append("")

    lines.append("## Tool Dependency Format Check")
    if non_toolid_format:
        lines.append("- status: `FAIL`")
        lines.append("```text")
        for m in non_toolid_format:
            lines.append(m)
        lines.append("```")
    else:
        lines.append("- status: `PASS`")
    lines.append("")

    lines.append("## Overlap (scope tags used by >1 active skill)")
    if overlap_rows:
        lines.append("| scope_tag | count | skills |")
        lines.append("|---|---:|---|")
        for r in overlap_rows:
            lines.append(f"| {r['scope_tag']} | {r['count']} | `{r['skills']}` |")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Missing-Capability Hints")
    if gap_hints:
        lines.append("| gap | suggested_skill | priority | reason |")
        lines.append("|---|---|---|---|")
        for r in gap_hints:
            lines.append(f"| {r['gap']} | `{r['suggested_skill']}` | {r['priority']} | {r['reason']} |")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## File-System Checks")
    lines.append("| skill | SKILL.md | openai.yaml | references/ |")
    lines.append("|---|---|---|---|")
    for r in fs_rows:
        lines.append(
            f"| {r['skill']} | {r['has_skill_md']} | {r['has_openai_yaml']} | {r['has_references_dir']} |"
        )
    lines.append("")
    lines.append("## Reference Topology Checks")
    lines.append("- policy: `each reference markdown should target one concrete situation; reference markdown count should stay <= 10 per skill`")
    lines.append("- heuristic: `documents > 200 lines are flagged as review-needed, not automatic violations`")
    lines.append("- heuristic: `SKILL.md > 80 lines with fewer than 2 reference docs is flagged as entry-too-heavy`")
    lines.append("| skill | SKILL.md lines | ref_md_count | >200_line_refs | count_status | single_case_risk | heavy_skill_entry_risk |")
    lines.append("|---|---:|---:|---:|---|---|---|")
    for r in ref_rows:
        lines.append(
            f"| {r['skill']} | {r['skill_md_lines']} | {r['ref_md_count']} | {r['long_ref_count_gt_200_lines']} | {r['ref_count_status']} | {r['single_case_risk']} | {r['heavy_skill_entry_risk']} |"
        )
    lines.append("")
    lines.append("## Artifacts")
    lines.append(f"- overlap_tsv: `{out_overlap}`")
    lines.append(f"- gaps_tsv: `{out_gap}`")
    lines.append(f"- fscheck_tsv: `{out_fs}`")
    lines.append(f"- refcheck_tsv: `{out_ref}`")
    lines.append(f"- summary_md: `{out_md}`")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote: {out_overlap}")
    print(f"wrote: {out_gap}")
    print(f"wrote: {out_fs}")
    print(f"wrote: {out_md}")
    print(f"entry_policy_ok={'YES' if entry_policy_ok else 'NO'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
