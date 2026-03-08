# EDA Preflight Reflection Artifact

Generate one markdown before any new run containing:
- root cause ranking (top 3),
- one-line hypothesis per root cause,
- one minimal A/B/C plan for the next run,
- explicit acceptance criteria.

Recommended helper script:

```bash
python3 scripts/debug/pre_experiment_reflection.py --case-tsv <case.tsv> --out-prefix <out_prefix>
```
