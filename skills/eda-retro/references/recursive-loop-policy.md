# Recursive Loop Policy

## Goal
Prevent blind repeated runs and enforce evidence-driven recursion.

## Recursion trigger (all required)
1. Next action has `confidence >= medium`.
2. Expected impact on target metric is `>= medium`.
3. Risk is bounded and explicitly acknowledged.
4. Required evidence for the next step is available or can be collected quickly.

## Recursion block (any one blocks)
1. Baseline/policy mismatch invalidates comparison.
2. Key metrics are missing or parsing is unstable.
3. Failure is primarily infrastructure/tool instability.
4. Proposed next step does not isolate one mechanism.

## Recursion payload
When recursion is approved, emit:
1. one-line objective,
2. fixed baseline and flow policy lock,
3. exact artifact paths for monitor/summary/gates,
4. stop condition and promotion condition.

## Exit condition
Stop recursive loop when one is true:
1. target objective met (for this stage),
2. two consecutive iterations fail the same gate without new mechanism evidence,
3. marginal gain is below threshold and cost is rising.
