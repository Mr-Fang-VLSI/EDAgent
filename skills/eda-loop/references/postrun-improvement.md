# Post-run Improvement Rule

## Trigger conditions
Apply at least one update when any condition is met:
1. Repeated manual steps appeared in this interaction.
2. A script/path/knob had to be rediscovered.
3. A gate/checklist item was ambiguous.
4. User clarified a policy that should become default.

## Preferred update order
1. Specialized sibling skill update/addition (preferred)
2. Knowledge base update (policy traceability)
3. Gate flow update (prevent recurrence)
4. Tool catalog refresh (discoverability)
5. `eda-loop` update or `agent.md` policy update (last resort)

## Orchestrator-update guard
Allow `eda-loop`/`agent.md` update only when:
1. The same orchestration gap appeared in >=2 interactions.
2. Updating a specialized skill cannot resolve it cleanly.
3. Proposed change is minimal and reversible.

## Minimal mandatory outputs
1. Maintenance log row.
2. Changed file paths.
3. New/updated artifact paths.
4. Open risks and next-step trigger condition.
5. If route/CTS was involved: unified preflight + execution-contract artifacts.
