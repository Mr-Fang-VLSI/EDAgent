# Literature Feedback Loop (Auto-Synced)

- timestamp: `2026-03-07 16:38:09`
- source_global_landscape: `docs/knowledge_base/index/global_research_landscape.tsv`
- papers_scanned: `15`
- stale_threshold: `latest_year <= 2023`

## Coverage Gaps
- missing_subproblems: `P3,P4,P5,P6,P7,P8`
- missing_methods: `M2,M4,M5,M6,M7`
- sparse_priority_pairs: `21`

## Stale Method Watchlist
| method_id | method | latest_year |
|---|---|---:|
| M2 | Local Resource-Aware Modeling | none |
| M4 | Constraint-Guided Optimization | none |
| M5 | A/B + Causal Validation | none |
| M6 | Stage-Gated Flow Integration | none |
| M7 | Legalization/DP Strategy | none |

## Targeted Retrieval Queue
- queue_path: `docs/papers/queues/literature_feedback_queue.tsv`
- queue_rows: `63`
- top_queries:
  - [high] P3+M1: timing-driven placement critical path placement objective multi-objective EDA backside last 5 years
  - [high] P3+M3: timing-driven placement critical path backside predictor cost model EDA backside last 5 years
  - [high] P3+M4: timing-driven placement critical path constrained optimization guardrail EDA backside last 5 years
  - [high] P4+M1: dynamic power switching power placement objective multi-objective EDA backside last 5 years
  - [high] P4+M3: dynamic power switching power backside predictor cost model EDA backside last 5 years
  - [high] P4+M4: dynamic power switching power constrained optimization guardrail EDA backside last 5 years
  - [high] P5+M1: nTSV via resistance placement objective multi-objective EDA backside last 5 years
  - [high] P5+M3: nTSV via resistance backside predictor cost model EDA backside last 5 years
  - [high] P5+M4: nTSV via resistance constrained optimization guardrail EDA backside last 5 years
  - [high] P6+M1: detailed placement legalization placement objective multi-objective EDA backside last 5 years
  - [high] P6+M3: detailed placement legalization backside predictor cost model EDA backside last 5 years
  - [high] P6+M4: detailed placement legalization constrained optimization guardrail EDA backside last 5 years

## Suggested Execution
1. Run `eda-paper-fetch` using top high-priority rows from queue.
2. Download/summarize new papers, then run `paper_kb_index.py build`.
3. Re-run this feedback script and compare gap/stale counts.
