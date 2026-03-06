# Autonomy Guardrails

## Planning autonomy
Allowed:
1. break user goal into executable phases,
2. submit and monitor jobs,
3. choose next action from observed evidence.

Not allowed:
1. changing comparison baselines without explicit note,
2. changing policy locks silently,
3. making promotion claims when required gates are pending.

## Self-improvement policy
Priority order:
1. update specialist skill,
2. update KB/gate/tooling,
3. update execution orchestrator skill (`eda-loop`) or `AGENTS.md` policy last.

Self-update trigger (all required):
1. repeated orchestration gap in >=2 interactions,
2. no clean fix by specialist skill updates,
3. minimal patch with clear rollback.

## Recursive loop trigger
Recursion is allowed only when:
1. high-confidence mechanism is identified,
2. next action isolates one factor,
3. expected impact is meaningful,
4. risk and runtime budget are acceptable.

## Mandatory artifact contract
Each loop must leave:
1. monitor artifact,
2. result summary,
3. retrospective note,
4. maintenance-log entry.
5. for model/cost updates: one derivative note (term definition + d/dx + smoothing bounds).
6. for route/CTS batches: one unified preflight artifact (`pdk_flow_preflight`).
7. for result claims: one execution-contract artifact (`validate_execution_contract`).
8. for continuing optimization: one experiment-memory/proposal artifact.
