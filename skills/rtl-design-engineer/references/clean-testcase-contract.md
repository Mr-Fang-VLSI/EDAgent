# Clean Testcase Contract

## Default Constraints

A default clean testcase should satisfy:
- synthesizable RTL only,
- no hard macro dependency,
- no external SRAM/fakeram requirement,
- no black-box leaf modules,
- small enough for fast place/CTS iteration,
- functionally meaningful enough to justify physical-design study.

## Promotion Checks

Before promoting the testcase, explicitly check for:
- memory macro wrappers (`fakeram`, generated SRAMs, `CLASS BLOCK` expectations),
- black-box placeholders,
- non-synthesizable constructs,
- accidental testbench dependencies,
- vendor-only primitives.

If the function inherently depends on macros, reject it as a clean testcase candidate and choose another block.
