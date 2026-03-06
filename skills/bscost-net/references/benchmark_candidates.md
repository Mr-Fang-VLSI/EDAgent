# Benchmark Candidates

Use this file to avoid overfitting to one design family.

## Core set
1. Existing systolic-array family used in this repo (`8x8/16x16/...`).
2. Rocket Chip generator (RISC-V SoC): https://github.com/chipsalliance/rocket-chip
3. Gemmini accelerator generator: https://github.com/ucb-bar/gemmini

## Optional expansion
1. Additional open CPU/SoC designs with diverse net topology.
2. Designs with deeper clock trees and longer global signal nets.

## Selection rule
1. Keep at least 3 design families in each stability report.
2. Include at least one CPU/SoC-style benchmark and one accelerator-style benchmark.
3. Freeze commit/release identifiers for reproducibility.
