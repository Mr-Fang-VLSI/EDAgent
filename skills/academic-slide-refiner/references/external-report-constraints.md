# Academic Slide Refiner External Report Constraints

For advisor-facing decks:
1. Use English only.
2. Remove internal or local markers from final slides:
- no absolute paths or local directory names,
- no long raw version tags,
- no internal host or user identifiers.
3. Prefer semantic experiment labels such as `Baseline`, `Variant-B`, or `Targeted-BM`.
4. If PDF is requested, prioritize `beamer` (`.tex -> .pdf`) and keep a source `.tex` artifact.
