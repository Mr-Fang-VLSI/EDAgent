# External Reporting Sanitization Checklist

Use this checklist for advisor/committee-facing slides.

## Content Sanitization
1. Use English throughout.
2. Replace local run IDs, timestamps, and ad-hoc tag names with semantic labels.
3. Remove local filesystem paths and host/user references.
4. Keep only meaningful identifiers (design name, experiment class, metric names).

## Narrative Scope
1. Restrict story to `Observation -> Problem -> Solution -> Result`.
2. Keep method names and metrics reproducible, but avoid internal tooling noise.
3. Report deltas/percentages with context and sign convention.

## Figure/Table Hygiene
1. No screenshots exposing IDE paths or shell prompts.
2. Captions should describe mechanism, not file names.
3. Use consistent labels (`Baseline`, `Variant A/B/C`, `Proposed`).

## Final Gate
1. One-page pass to check accidental local leakage.
2. Confirm all references are publishable/meeting-safe.
