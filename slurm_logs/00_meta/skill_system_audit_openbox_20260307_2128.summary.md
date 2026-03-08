# Skill System Audit

- timestamp: `2026-03-07 21:25:59`
- manifest: `skills/00_SKILL_SYSTEM_MANIFEST.tsv`
- agent_md: `AGENTS.md`
- agent_md_exists: `YES`
- active_entry_skills: `none`
- entry_policy_rule: `AGENTS.md must exist; active entry skills <=1; no compatibility entry skill is required`
- entry_policy_ok: `YES`

## Dependency Check
- status: `PASS`

## Version Contract Check
- status: `PASS`

## Tool Dependency Path Check
- tool_catalog: `docs/tool_registry/tool_catalog.tsv`
- known_tool_id_count: `198`
- status: `PASS`

## Tool Dependency Format Check
- status: `PASS`

## Overlap (scope tags used by >1 active skill)
| scope_tag | count | skills |
|---|---:|---|
| promotion_gate | 2 | `bspdn-goal-driver,eda-hypothesis-experiment-designer` |

## Missing-Capability Hints
| gap | suggested_skill | priority | reason |
|---|---|---|---|
| portfolio_planning | `eda-portfolio-manager` | high | No skill explicitly manages multi-batch prioritization/resource budgeting. |
| result_warehouse | `eda-results-regression` | high | No dedicated skill for normalized experiment database/golden regression snapshots. |
| visual_insight | `eda-viz-insight` | medium | No dedicated skill for standardized visual diagnostics and publication-ready plots. |

## File-System Checks
| skill | SKILL.md | openai.yaml | references/ |
|---|---|---|---|
| academic-presentation-crafter | yes | yes | yes |
| academic-slide-refiner | yes | yes | yes |
| backside-benefit-attribution-evaluator | yes | yes | yes |
| backside-routing-realization-specialist | yes | yes | yes |
| eda-artifact-hygiene-maintainer | yes | yes | yes |
| bscost-net | yes | yes | yes |
| bscost-theory-opt | yes | yes | yes |
| bspdn-pdn-sufficiency-evaluator | yes | yes | yes |
| bspdn-physical-contract-auditor | yes | yes | yes |
| bspdn-goal-driver | yes | yes | yes |
| delay-model-gate-evaluator | yes | yes | yes |
| eda-context-accessor | yes | yes | yes |
| eda-autoidea-bridge | yes | yes | yes |
| eda-experiment-phenomenology-analyst | yes | yes | yes |
| eda-script-pattern-curator | yes | yes | yes |
| eda-hypothesis-experiment-designer | yes | yes | yes |
| eda-idea-debate-lab | yes | yes | yes |
| eda-infra-maintainer | yes | yes | yes |
| control-knowledge-explorer | yes | yes | yes |
| eda-knowledge-gate-maintainer | yes | yes | yes |
| workflow-scoped-execution | yes | yes | yes |
| eda-method-implementer | yes | yes | yes |
| eda-paper-fetch | yes | yes | yes |
| eda-pdf-local-summary | yes | yes | yes |
| control-preflight-reflect | yes | yes | yes |
| workflow-research-chain | yes | yes | yes |
| control-postrun-retro | yes | yes | yes |
| conda-project-environment-manager | yes | yes | yes |
| eda-stage-checkpoint-golden | yes | yes | yes |
| eda-system-packager | yes | yes | yes |
| control-theory-veto | yes | yes | yes |
| git-version-control | yes | yes | yes |
| gt3-backside-route-policy | yes | yes | yes |
| rtl-design-engineer | yes | yes | yes |
| workflow-router | yes | yes | yes |
| gt3-backside-net-selector | yes | yes | yes |

## Reference Topology Checks
- policy: `each reference markdown should target one concrete situation; reference markdown count should stay <= 10 per skill`
- heuristic: `documents > 200 lines are flagged as review-needed, not automatic violations`
- heuristic: `SKILL.md > 80 lines with fewer than 2 reference docs is flagged as entry-too-heavy`
| skill | SKILL.md lines | ref_md_count | >200_line_refs | count_status | single_case_risk | heavy_skill_entry_risk |
|---|---:|---:|---:|---|---|---|
| academic-presentation-crafter | 73 | 3 | 0 | PASS | OK | OK |
| academic-slide-refiner | 23 | 5 | 0 | PASS | OK | OK |
| backside-benefit-attribution-evaluator | 60 | 2 | 0 | PASS | OK | OK |
| backside-routing-realization-specialist | 84 | 2 | 0 | PASS | OK | OK |
| eda-artifact-hygiene-maintainer | 81 | 7 | 0 | PASS | OK | OK |
| bscost-net | 31 | 6 | 0 | PASS | OK | OK |
| bscost-theory-opt | 37 | 4 | 0 | PASS | OK | OK |
| bspdn-pdn-sufficiency-evaluator | 56 | 2 | 0 | PASS | OK | OK |
| bspdn-physical-contract-auditor | 57 | 2 | 0 | PASS | OK | OK |
| bspdn-goal-driver | 36 | 5 | 0 | PASS | OK | OK |
| delay-model-gate-evaluator | 39 | 1 | 0 | PASS | OK | OK |
| eda-context-accessor | 62 | 4 | 0 | PASS | OK | OK |
| eda-autoidea-bridge | 36 | 0 | 0 | PASS | OK | OK |
| eda-experiment-phenomenology-analyst | 80 | 2 | 0 | PASS | OK | OK |
| eda-script-pattern-curator | 65 | 2 | 0 | PASS | OK | OK |
| eda-hypothesis-experiment-designer | 35 | 3 | 0 | PASS | OK | OK |
| eda-idea-debate-lab | 40 | 1 | 0 | PASS | OK | OK |
| eda-infra-maintainer | 85 | 8 | 0 | PASS | OK | OK |
| control-knowledge-explorer | 44 | 1 | 0 | PASS | OK | OK |
| eda-knowledge-gate-maintainer | 72 | 5 | 0 | PASS | OK | OK |
| workflow-scoped-execution | 78 | 4 | 0 | PASS | OK | OK |
| eda-method-implementer | 51 | 1 | 0 | PASS | OK | OK |
| eda-paper-fetch | 51 | 2 | 0 | PASS | OK | OK |
| eda-pdf-local-summary | 60 | 2 | 0 | PASS | OK | OK |
| control-preflight-reflect | 30 | 4 | 0 | PASS | OK | OK |
| workflow-research-chain | 50 | 3 | 0 | PASS | OK | OK |
| control-postrun-retro | 75 | 2 | 0 | PASS | OK | OK |
| conda-project-environment-manager | 61 | 2 | 0 | PASS | OK | OK |
| eda-stage-checkpoint-golden | 50 | 1 | 0 | PASS | OK | OK |
| eda-system-packager | 69 | 4 | 0 | PASS | OK | OK |
| control-theory-veto | 58 | 3 | 0 | PASS | OK | OK |
| git-version-control | 69 | 4 | 0 | PASS | OK | OK |
| gt3-backside-route-policy | 41 | 1 | 0 | PASS | OK | OK |
| rtl-design-engineer | 48 | 3 | 0 | PASS | OK | OK |
| workflow-router | 71 | 5 | 0 | PASS | OK | OK |
| gt3-backside-net-selector | 58 | 2 | 0 | PASS | OK | OK |

## Artifacts
- overlap_tsv: `slurm_logs/00_meta/skill_system_audit_openbox_20260307_2128.overlap.tsv`
- gaps_tsv: `slurm_logs/00_meta/skill_system_audit_openbox_20260307_2128.gaps.tsv`
- fscheck_tsv: `slurm_logs/00_meta/skill_system_audit_openbox_20260307_2128.fscheck.tsv`
- refcheck_tsv: `slurm_logs/00_meta/skill_system_audit_openbox_20260307_2128.refcheck.tsv`
- summary_md: `slurm_logs/00_meta/skill_system_audit_openbox_20260307_2128.summary.md`
