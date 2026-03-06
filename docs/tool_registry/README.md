# Tool Registry

This directory is a searchable and governable registry for local tools, flow scripts, and stage scripts.

## Files
- `tool_catalog.tsv`: machine-readable table.
- `tool_catalog.md`: human-readable grouped index.
- `tool_metadata.tsv`: optional authoritative metadata overlay (`tool_id`, `version`, `owner`, `lifecycle`, contracts, validation evidence).

## Build / Refresh
Run:

```bash
python3 scripts/common/tool_catalog.py build
```

## Query
Run:

```bash
python3 scripts/common/tool_catalog.py query cts route
python3 scripts/common/tool_catalog.py query innovus --type flow_stage
python3 scripts/common/tool_catalog.py query monitor --stage analysis --lifecycle active
```

## Intended workflow
Before creating a new script:
1. query the catalog for related tools,
2. reuse existing script if suitable,
3. only add new script when gap is confirmed.

## Governance fields
The catalog now tracks these lifecycle fields per tool:
- `tool_id`
- `lifecycle` (`active` / `deprecated` / `experimental`)
- `version` (semantic version)
- `owner`
- `domain`, `stage`
- `input_contract`, `output_contract`
- `validator`, `last_verified`, `evidence_path`
- `replacement_tool_id` (for deprecation migration)

## Skill integration rule
- `skills/00_SKILL_SYSTEM_MANIFEST.tsv:depends_on_tools` must reference `tool_id` values from `tool_catalog.tsv` (except external allowlist like `git/node/python3/bash`).
