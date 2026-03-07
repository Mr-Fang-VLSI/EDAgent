# EDA Loop Output And Stop Policy

## Required Outputs

Return or update:
- canonical monitor path,
- canonical manifest path,
- key artifact paths,
- execution verdict,
- next constrained action.

## Hard-stop Conditions

Do not close the task if any are true:
1. No maintenance-log update for the interaction.
2. No tool-catalog query evidence for non-trivial changes.
3. Artifacts were created but not linked in the final summary.
4. Skill changed but was not validated.
5. Algorithmic claim was made without `vanilla_replace` primary baseline.
6. Route/CTS batch was referenced without unified preflight artifact.
7. Route-level conclusion was given while execution-contract FAIL rows remain unresolved.
8. Submitted jobs were not accompanied by explicit monitor/manifest/job-id reporting.
