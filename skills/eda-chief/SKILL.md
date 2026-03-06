---
name: eda-chief
description: Legacy compatibility shim for historical eda-chief calls. Use when old prompts/scripts still invoke eda-chief, then dispatch to the repo-level agent policy and execution skills.
---

# EDA Chief

## Role

`eda-chief` is no longer the primary orchestrator.
It is a compatibility layer for older workflows that still call this skill name.

Top-level governance is defined in `agent.md` at repo root.

## What to do when invoked

1. Load `agent.md` and follow its global routing/governance policy.
2. Convert legacy "chief-style" request into a scoped execution brief.
3. Dispatch execution to `eda-loop`.
4. Add control skills only when needed:
   - `eda-theory-veto` for high-cost/high-risk proposals.
   - `eda-retro` after experiment batches that need next-step decision.
5. Keep outputs short and artifact-driven.

## Hard boundaries

1. Do not redefine global entry policy inside this skill.
2. Do not duplicate global recursion/self-update policy from `agent.md`.
3. Prefer domain skills for domain reasoning and implementation.
4. Mention compatibility mode explicitly when this skill is used.

## References

Load only when needed:
1. `references/delegation-matrix.md`
2. `references/autonomy-guardrails.md`
