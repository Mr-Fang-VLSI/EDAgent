# KB Context Loading

## Purpose

Load only the knowledge-base context that is needed for the current task and convert it into a compact artifact for downstream skills.

## Procedure

1. Read the task brief or scoped objective first.
2. Identify the minimum KB files needed for this task.
3. If indexed retrieval is useful, run:

```bash
python3 scripts/common/unified_kb_query.py build
python3 scripts/common/unified_kb_query.py query --source all --mode hybrid --query "<query>"
```

4. Summarize the retrieved KB evidence into a scoped note such as `kb_context.md`.

## Guardrails

1. Prefer file/path-level references for key claims.
2. Separate confirmed evidence from open questions or unresolved contradictions.
