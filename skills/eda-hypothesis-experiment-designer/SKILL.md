---
name: eda-hypothesis-experiment-designer
description: Convert research ideas into falsifiable hypotheses and experiment plans with metrics, controls, pass/fail criteria, and confounder mitigation.
---

# EDA Hypothesis Experiment Designer

## When to use

Use this skill after idea selection and before method implementation or expensive experiment submission.

## Workflow

1. Extract key assumptions from idea memo.
2. Translate each assumption into a falsifiable hypothesis.
3. Build an experiment matrix:
- hypothesis ID,
- manipulation,
- control/baseline,
- metrics,
- expected direction,
- pass/fail threshold,
- confounders and mitigation.
4. Define minimum sample panel and runtime budget.
5. Mark promotion gate:
- what evidence is required to move from hypothesis to implementation.

## Outputs

1. `hypothesis_experiment_matrix.tsv`
2. `experiment_design_note.md`
3. `promotion_gate.md`

## Hard rules

1. Each hypothesis must have explicit disproof condition.
2. Metrics must match decision question (not just easy-to-collect metrics).
3. Include at least one negative-control or ablation check when feasible.

## Reference

Load when needed:
1. `references/matrix-rules.md`
