---
name: eda-theory-veto
description: Theory-level veto skill for EDA plans. Use before expensive experiment submissions or major flow/model changes to identify logically unsound assumptions, contradiction with known physics/policy, and high-risk invalid comparisons. Produces GO/CONDITIONAL/NO-GO with evidence.
---

# EDA Theory Veto

## Overview

This skill protects the loop from executing invalid ideas just because they are executable.
It evaluates proposal validity against theory, known constraints, and policy, then emits a veto decision.

## When to run

Run before:
1. launching large/long job batches,
2. changing objective/cost model assumptions,
3. making algorithmic comparison claims,
4. introducing new route/CTS/PDN policy that may break prior assumptions.

## Inputs

Required:
1. current user proposal (one-paragraph objective),
2. relevant artifacts (latest summary/gate/monitor),
3. KB references used by the proposal.

Recommended:
1. primary-source/web references when assumptions may drift.

## Workflow

1. Parse proposal into falsifiable assumptions.
2. Check each assumption against:
   - known physics/EDA constraints,
   - local policy locks (comparison, route policy),
   - current empirical evidence.
3. Classify conflicts:
   - hard contradiction,
   - missing evidence,
   - plausible but high-risk.
4. Emit one verdict:
   - `GO`: no blocking contradiction.
   - `CONDITIONAL`: proceed only with listed constraints.
   - `NO-GO`: block execution; provide minimum fix path.
5. Provide minimal corrective experiment if vetoed.

## Decision output contract

Always output:
1. `verdict`: GO / CONDITIONAL / NO-GO
2. `blocking_reasons`: numbered list
3. `assumption_table`: assumption, evidence, status
4. `safe_next_step`: one minimal testable action
5. `override_policy`:
   - NO-GO can be bypassed only with explicit user override.
   - when override happens, mark run as `veto_overridden`.

## References

Load:
1. `references/veto-criteria.md`
2. `references/decision-template.md`
