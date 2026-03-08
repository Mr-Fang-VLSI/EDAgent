# Veto Criteria

Use these checks in order.

## 1) Physics/model consistency
NO-GO if:
1. proposal contradicts known RC/via/capacity behavior without new evidence.
2. objective assumes monotonic benefit where prior data shows opposite regime behavior.

CONDITIONAL if:
1. mechanism is plausible but only in a limited regime (e.g., long nets only).

## 2) Comparison-policy consistency
NO-GO if:
1. algorithmic superiority is claimed without `vanilla_replace` primary baseline.
2. compared variants have mismatched downstream route policy.

## 3) Evidence sufficiency
NO-GO if:
1. key target metrics cannot be measured from planned artifacts.
2. plan lacks identifiable A/B factor isolation.

CONDITIONAL if:
1. evidence exists but sample size/regime coverage is weak.

## 4) Repeated empirical experience
NO-GO if:
1. the same branch has already failed multiple times with the same dominant mechanism and the new plan does not introduce a meaningful new control variable.
2. prior batches already showed the proposal cannot satisfy the intended admission claim (for example backside use too weak for a claimed backside-benefit testcase), and the new plan is effectively identical.

CONDITIONAL if:
1. experience indicates high risk, but a smaller diagnostic run can still isolate whether the old failure pattern remains.

## 5) Resource/risk sanity
CONDITIONAL or NO-GO if:
1. compute cost is high with low expected information gain.
2. likely outcome is ambiguous because multiple knobs change at once.

## 6) Override policy
If verdict is NO-GO:
1. default action: block submission.
2. allow proceed only with explicit user override and mark result as `veto_overridden`.
