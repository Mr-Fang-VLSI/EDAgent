# Package Build

Use this reference when building the standalone agent+skill bundle.

## Standard Command

```bash
python3 scripts/common/build_agent_skill_bundle.py --out-dir exports/eda_agent_skill_system
```

## Output Location Rule

1. Use the requested output directory when provided.
2. Otherwise default to `exports/eda_agent_skill_system`.
3. Record the final output path in the packaging summary.
