# RTL Testcase Package And Validation

## Standard Package

A clean testcase package should contain:
- `rtl/` with the dependency-closed RTL set,
- `manifest.tsv` listing source provenance,
- `top.txt` with the chosen top module,
- `constraints.sdc` with a minimal realistic clock contract,
- `notes.md` summarizing:
  - function,
  - why it is meaningful,
  - why it qualifies as macro-free,
  - known limitations.

Keep naming stable so later synthesis/P&R scripts can consume it automatically.

## Minimum Validation Before Handoff

1. dependency closure is complete,
2. clean testcase contract is satisfied,
3. top module and clock/reset interface are explicit,
4. provenance is recorded,
5. limitations are recorded.

For testcase packages intended for the default DC/Innovus flow, also require:

```bash
python3 scripts/common/check_design_package.py --design <design> --require-design-top-match --out-md <report.md>
```

This prevents the common failure mode where the flow launches with design name `<design>` but the packaged RTL top is a different module, which later surfaces as DC `LBR-0` / "Cannot find the design" errors.

If local lint/syntax tools are available, run them. If not, state that validation is structural only.
