# Tool Reuse Query

## Purpose

Check the tool registry before a downstream skill adds a new script, wrapper, parser, validator, or reporting helper.

## Procedure

Run:

```bash
python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>
```

Record:
- query terms,
- candidate reusable tools,
- reuse decision,
- gap note if no suitable tool exists.

## Guardrails

1. Reuse existing tools when the fit is adequate.
2. If no tool fits, state the gap explicitly so downstream maintenance or implementation skills can act on it.
