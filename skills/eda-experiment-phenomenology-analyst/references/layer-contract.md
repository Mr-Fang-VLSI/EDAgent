# Layer Contract

Use this contract to keep experiment-evidence lifting consistent.

## 1) Log layer

Contains raw sources only:
- stdout/stderr logs,
- reports,
- monitor/history,
- manifests,
- tool-generated summaries.

No interpretation belongs here.

## 2) Result layer

Contains directly extracted facts:
- timing (`WNS/TNS/ViolPaths`)
- PPA (`power/area/runtime`)
- route/geometry (`backside nets`, `selected ratio`, `overflow`, `HPWL`)
- gate status and stage reached

Rules:
1. prefer machine-parseable tables or JSON,
2. do not attach mechanism labels yet,
3. normalize units before comparison and note any ambiguity.

## 3) Conclusion layer

Contains batch-local mechanism judgments:
- what dominated the outcome,
- what was ruled out,
- what the next smallest useful diagnostic or promotion step is.

Rules:
1. every conclusion must cite concrete `result` items,
2. conclusions may be high-confidence or provisional,
3. conclusions do not automatically become durable experience.

## 4) Experience layer

Contains reusable cross-batch patterns only when evidence is strong enough.

Each experience item should capture:
1. `experience_id`
2. `scope`
3. `trigger_pattern`
4. `evidence_runs`
5. `confidence`
6. `recommendation`
7. `veto_implication`
8. `last_seen`
9. `owner_skill`

Promote into `experience` when at least one of these is true:
1. the same mechanism appears repeatedly across related batches,
2. one batch yields unusually decisive evidence with clear trigger and consequence,
3. a repeated user/governance principle requires durable reuse.
