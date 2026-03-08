# Research Chain Stage Flow

Use this file after `SKILL.md` has selected `workflow-research-chain`.

`workflow-research-chain` remains the workflow owner across all stages below.
Use `workflow-scoped-execution` only for the specific execution/validation stages that need governed execution wrapping.

## Bootstrap

Initialize chain workspace:

```bash
python3 scripts/common/init_research_chain.py --tag <tag>
```

## Stage Sequence

1. Knowledge exploration:
- use `control-knowledge-explorer` to map local knowledge gaps,
- produce `01_knowledge/knowledge_gap_map.md`.

2. Literature retrieval and local parsing:
- use `eda-paper-fetch` to generate download queue,
- use `eda-pdf-local-summary` after local PDFs are available,
- produce `02_literature/paper_download_queue.tsv` and `02_literature/local_paper_summary_index.md`.

3. Idea brainstorming and debate:
- use `eda-idea-debate-lab`,
- produce `03_idea_debate/idea_brainstorm.md` and `03_idea_debate/pro_con_debate.md`.

4. Hypothesis to experiment design:
- use `eda-hypothesis-experiment-designer`,
- run `control-preflight-reflect` before expensive submissions,
- produce `04_hypothesis_design/hypothesis_experiment_matrix.tsv`.

5. Method implementation:
- use `eda-method-implementer`,
- produce `05_implementation/implementation_plan.md`.

6. Multi-version development and integration:
- use `git-version-control`,
- produce `06_versioning/version_plan.md` and version delta notes.

7. Validation and decision:
- execute via `workflow-scoped-execution`,
- use validation tools/skills such as `delay-model-gate-evaluator` and execution-contract checks,
- produce `07_validation/validation_summary.md`.

8. Retrospective:
- use `control-postrun-retro`,
- produce `08_retro/research_retro.md`.

## Completeness Guard

After stage execution, run:

```bash
python3 scripts/common/research_chain_guard.py --chain-dir <chain_dir> --out-prefix <prefix>
```
