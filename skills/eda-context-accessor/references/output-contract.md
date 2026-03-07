# Context Output Contract

## Minimal Artifact Set

Provide a compact handoff containing:
1. task scope,
2. KB files or retrieval results actually used,
3. tool-query evidence,
4. reuse recommendation,
5. open evidence gaps,
6. `kb_feedback_decision`,
7. `kb_feedback_reason`.

## Preferred Artifact Shapes

- `kb_context.md`
- `tool_query_note.md`
- or one combined scoped context note if the task is small

## Handoff Rule

Downstream skills should consume this artifact instead of re-running the same KB/tool lookup unless the scope changed materially.

They must also explicitly consume the KB feedback field by either:
- requesting KB/infrastructure maintenance,
- updating a KB-facing log or artifact,
- or recording that the correct decision is `none`.
