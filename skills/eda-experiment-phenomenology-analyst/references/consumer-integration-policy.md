# Consumer Integration Policy

Use this reference when another skill wants to consume the experience layer.

## `workflow-scoped-execution`

Use after a batch or diagnostic stage completes and the outcome should survive the current turn.

Expected handoff:
1. generate `result`,
2. generate `conclusion`,
3. generate `experience_delta` only if a reusable pattern emerged,
4. pass those artifacts forward to `control-postrun-retro` or later planning.

## `control-postrun-retro`

Use structured `result/conclusion` as the default starting point.

Expected behavior:
1. do not rebuild the registry,
2. decide next step based on the strongest available conclusion,
3. cite any reused experience item explicitly.

## `control-theory-veto`

Use `experience` as an additional input, not as a replacement for theory or policy.

Expected behavior:
1. cite repeated empirical patterns that raise risk,
2. issue `CONDITIONAL` when experience suggests a smaller diagnostic is still valuable,
3. issue `NO-GO` when the same weak-information or failed branch is being repeated without a meaningful new control variable.

## `workflow-research-chain`

Use when a chain stage finishes and its evidence should be reusable by later stages or later chains.

Expected behavior:
1. store chain-local artifacts,
2. link validated experience back into durable project memory,
3. keep experience extraction separate from retrospective stage ownership.
