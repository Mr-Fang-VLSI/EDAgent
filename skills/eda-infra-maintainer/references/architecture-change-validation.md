# Architecture Change Validation

Use this reference when a maintenance or development task changes routing, skill boundaries, workflow ownership, or reference topology policy.

## Required Capture

Record all four items:
1. change hypothesis: what problem the architecture change is supposed to reduce,
2. expected benefit: what should become faster, clearer, smaller, or easier to maintain,
3. validation window: when or after how many interactions the change should be reviewed,
4. falsification signal: what evidence would show the architecture change did not help.

## Suggested Validation Signals

Use only the signals relevant to the change:
1. fewer duplicated rules across `AGENTS.md`, `SKILL.md`, and refs,
2. lower `heavy_skill_entry_risk` or ref-topology warnings in `skill_system_audit`,
3. fewer routing ambiguities about which skill owns a workflow,
4. fewer cases where utility logic is copied into execution/theory skills,
5. lower need to patch multiple skills for one horizontal policy change,
6. clearer artifact and owner reporting in maintenance logs.

## Output Requirement

For architecture changes, leave behind:
1. one KB note or SOP entry describing the change rationale,
2. one explicit later-review plan,
3. one maintenance-log entry mentioning how success will be evaluated later.
