---
name: eda-research-chain
description: Run a full EDA research chain from knowledge exploration and paper triage to idea debate, hypothesis experiment design, implementation, git versioning, validation, and retrospective.
---

# EDA Research Chain

## When to use

Use this skill when the user asks for an end-to-end research workflow, not a single isolated experiment step.

## Scope

This skill orchestrates the full chain and delegates each stage to specialized skills.
Global governance still follows `agent.md`.

## Stage flow

1. Bootstrap chain workspace:

```bash
python3 scripts/common/init_research_chain.py --tag <tag>
```

2. Knowledge exploration:
- use `eda-knowledge-explorer` to map local knowledge gaps,
- produce `01_knowledge/knowledge_gap_map.md`.

3. Literature retrieval + local parsing:
- use `eda-paper-fetch` to generate download queue,
- use `eda-pdf-local-summary` after local PDFs are available,
- produce `02_literature/paper_download_queue.tsv` and `02_literature/local_paper_summary_index.md`.

4. Idea brainstorming and debate:
- use `eda-idea-debate-lab`,
- produce `03_idea_debate/idea_brainstorm.md` and `03_idea_debate/pro_con_debate.md`.

5. Hypothesis -> experiment design:
- use `eda-hypothesis-experiment-designer`,
- run `eda-preflight-reflect` before expensive submissions,
- produce `04_hypothesis_design/hypothesis_experiment_matrix.tsv`.

6. Method implementation:
- use `eda-method-implementer`,
- produce `05_implementation/implementation_plan.md`.

7. Multi-version development and integration:
- use `git-version-control`,
- produce `06_versioning/version_plan.md` and version delta notes.

8. Validation and decision:
- execute via `eda-loop`,
- use validation tools/skills (`delay-model-gate-evaluator`, execution contract),
- produce `07_validation/validation_summary.md`.

9. Retrospective:
- use `eda-retro`,
- produce `08_retro/research_retro.md`.

10. Version milestone summary slides (conditional):
- do not generate slides for every process stage by default.
- generate a PDF summary only when a new version achieves a validated milestone improvement (e.g., first reach `>=2%` power reduction with non-worse area/timing, then higher milestones).
- summary should include: method delta, key conclusion, evidence table, and next-step plan.

11. Guard completeness:

```bash
python3 scripts/common/research_chain_guard.py --chain-dir <chain_dir> --out-prefix <prefix>
```

## Hard rules

1. Do not skip the hypothesis design stage before implementation.
2. Do not promote a method without explicit validation artifact.
3. Keep each stage artifact path explicit and auditable.
4. If critical guard checks fail, block chain completion.

## Reference

Load when needed:
1. `references/chain-checklist.md`
