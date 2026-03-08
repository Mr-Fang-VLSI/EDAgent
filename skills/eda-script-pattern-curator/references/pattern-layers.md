# Pattern Layers

Use this contract to lift script-writing experience without mixing it with experiment results.

## 1) Incident

Concrete script event:
- wrapper broke,
- runtime mismatch,
- duplicated parser logic,
- missing guard or reporting field,
- one-off helper became reused.

## 2) Local fix

What changed in the specific script:
- path handling fix,
- argument normalization,
- explicit `python3.11` wrapper,
- stricter postcheck,
- catalog metadata update.

## 3) Pattern

Promote only when the lesson is reusable:
- when to introduce a common helper,
- when to keep logic local,
- when runtime pinning is mandatory,
- when wrapper output contracts should be standardized.

## 4) Anti-pattern

Capture durable “do not repeat” cases:
1. creating a new wrapper before querying the tool catalog,
2. silent runtime assumptions in mixed cluster environments,
3. embedding shared parsing logic in multiple ad hoc scripts,
4. changing output schema without updating downstream consumers.
