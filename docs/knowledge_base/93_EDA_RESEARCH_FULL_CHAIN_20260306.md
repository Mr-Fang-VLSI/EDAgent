# 93 EDA Research Full Chain (2026-03-06)

## Goal
Create a reproducible end-to-end research chain for EDA work:
1. knowledge exploration,
2. paper retrieval guidance for local download,
3. local paper parsing,
4. idea brainstorming and pro/con debate,
5. hypothesis-to-experiment design,
6. method implementation,
7. git-based multi-version integration,
8. validation and final decision.

## Core skill chain
1. `eda-research-chain` (overall chain orchestration)
2. `eda-knowledge-explorer` (knowledge gap mapping)
3. `eda-paper-fetch` (paper candidate queue for local download)
4. `eda-pdf-local-summary` (local PDF parsing and summary)
5. `eda-idea-debate-lab` (brainstorm + structured debate)
6. `eda-hypothesis-experiment-designer` (falsifiable experiment matrix)
7. `eda-method-implementer` (implementation from approved hypothesis)
8. `git-version-control` (multi-version checkpoints and integration records)
9. `eda-loop` + validation tools/skills (execution + contract checks)
10. `eda-retro` (post-run mechanism and next-step decision)
11. `bspdn-goal-driver` (goal milestone tracking and campaign gating)

## Workspace initialization
```bash
python3 scripts/common/init_research_chain.py --tag <tag>
```

## Completeness guard
```bash
python3 scripts/common/research_chain_guard.py --chain-dir slurm_logs/05_research_chain/<tag> --out-prefix slurm_logs/00_meta/research_chain_guard_<tag>
```

## Mandatory deliverables per chain
1. `knowledge_gap_map.md`
2. `paper_download_queue.tsv`
3. `local_paper_summary_index.md`
4. `idea_brainstorm.md`
5. `pro_con_debate.md`
6. `hypothesis_experiment_matrix.tsv`
7. `implementation_plan.md`
8. `version_plan.md`
9. `validation_summary.md`
10. `research_retro.md`

## Hard promotion rule
Do not promote any method/idea unless validation summary includes explicit go/no-go with linked evidence paths.
