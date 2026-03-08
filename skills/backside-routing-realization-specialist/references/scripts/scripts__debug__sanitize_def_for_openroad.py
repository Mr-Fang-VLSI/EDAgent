#!/usr/bin/env python3.11
"""Sanitize an Innovus DEF into an OpenROAD-friendly routed DEF.

This is intentionally narrow. It strips three syntax/features that have been
observed to break OpenROAD DEF import for GT3 routed outputs in this repo:
1. `NONDEFAULTRULES ... END NONDEFAULTRULES`
2. inline `TAPERRULE WidthRule*` tokens on routed wire statements
3. inline `VIRTUAL` route markers on routed wire statements

The goal is compatibility for OpenROAD/OpenDB patch tooling, not fidelity to
all Innovus DEF features.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NDR_BLOCK_RE = re.compile(
    r"(?ms)^NONDEFAULTRULES\s+\d+\s*;\n.*?^END NONDEFAULTRULES\s*$\n?"
)
TAPER_RE = re.compile(r"(\s+)TAPERRULE(\s+)WidthRule\d+")
VIRTUAL_RE = re.compile(r"(\s+)VIRTUAL(?=(\s+[A-Z_]+\b|\s+\(|\s*;))")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--in-def", required=True)
    p.add_argument("--out-def", required=True)
    p.add_argument(
        "--keep-ndrs",
        action="store_true",
        help="Do not remove the NONDEFAULTRULES block.",
    )
    p.add_argument(
        "--keep-taperrules",
        action="store_true",
        help="Do not strip TAPERRULE WidthRule* route tokens.",
    )
    p.add_argument(
        "--keep-virtual",
        action="store_true",
        help="Do not strip VIRTUAL route markers.",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    in_def = Path(args.in_def)
    out_def = Path(args.out_def)
    text = in_def.read_text(encoding="utf-8", errors="ignore")

    removed_ndr_blocks = 0
    stripped_taperrules = 0
    stripped_virtual = 0

    if not args.keep_ndrs:
        text, removed_ndr_blocks = NDR_BLOCK_RE.subn("", text, count=1)

    if not args.keep_taperrules:
        text, stripped_taperrules = TAPER_RE.subn(r"\1", text)

    if not args.keep_virtual:
        text, stripped_virtual = VIRTUAL_RE.subn(r"\1", text)

    out_def.parent.mkdir(parents=True, exist_ok=True)
    out_def.write_text(text, encoding="utf-8")

    print(f"input={in_def}")
    print(f"output={out_def}")
    print(f"removed_ndr_blocks={removed_ndr_blocks}")
    print(f"stripped_taperrules={stripped_taperrules}")
    print(f"stripped_virtual={stripped_virtual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
