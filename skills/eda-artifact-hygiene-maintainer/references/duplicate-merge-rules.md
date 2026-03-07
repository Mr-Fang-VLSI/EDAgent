# Duplicate Merge Rules

Merge artifacts when all of the following are true:
1. they serve the same operational purpose,
2. one is clearly a superset or refined replacement of the other,
3. keeping both adds confusion rather than traceability.

Do not merge when:
1. the files represent different experimental states or historical checkpoints,
2. the distinction is important for causal reconstruction,
3. one file is generated and the other is hand-curated with different roles.

When merging:
1. identify the canonical surviving artifact,
2. record which files were absorbed,
3. preserve any unique evidence that would otherwise be lost.
