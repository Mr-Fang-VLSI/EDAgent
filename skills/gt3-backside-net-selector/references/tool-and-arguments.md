# GT3 Backside Net Selector Tool And Arguments

Prefer:

```bash
python3 scripts/debug/select_backside_nets_power_first.py \
  --def-file <postcts_or_place_def> \
  --out-prefix <artifact_prefix> \
  --techlef-file <techlef> \
  --capacity-ratio 0.08 \
  --topk-total 128
```

Optional:
- `--criticality-file <tsv>` for timing-safety screening,
- `--activity-file <tsv>` when real toggle/activity data is available,
- `--include-clock` if clock nets are part of the migration policy.
