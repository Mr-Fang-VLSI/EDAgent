# Update Mechanism

Refresh this skill's summarized knowledge when:

## Refresh triggers

1. a new oracle/manual/OpenROAD reroute experiment changes the current understanding of `selection bookkeeping` vs real `BM2/BM1` occupancy
2. the local rerouter gains a stable OpenROAD/OpenDB route-spec format
3. extraction-friendly patched nets become measurable and change the interpretation of current route-realization blockers
4. Gate B or later routing-realization work reveals that the current failure is actually caused by physical-contract invalidity rather than rerouter implementation
5. the local code structure changes enough that the skill's code-entry references are no longer the best repair points

## What to update

1. refresh `background-knowledge-links.md`
2. update the route-realization notes in `docs/knowledge_base/107_BSPDN_TOPOLOGY_AND_BENEFIT_VALIDATION_PROGRAM_20260307.md`
3. promote repeated routing-realization lessons into experiment or script experience artifacts
4. update the tool references when the preferred rerouter path changes from raw patching to OpenROAD/OpenDB-backed rewriting
5. refresh the "local code structure" section when repair ownership moves between scripts or helper layers

## Promotion rule

Only revise the routing-realization story when repeated experiments change the dominant blocker.
Do not rewrite the story from one unstable or extraction-broken patch attempt.
