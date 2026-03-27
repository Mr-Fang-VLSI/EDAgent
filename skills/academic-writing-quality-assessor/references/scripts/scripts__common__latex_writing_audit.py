#!/usr/bin/env python3
"""Mirrored copy of scripts/common/latex_writing_audit.py for portable skill bundles."""

from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / "scripts" / "common" / "latex_writing_audit.py"

if __name__ == "__main__":
    sys.argv[0] = str(SCRIPT)
    runpy.run_path(str(SCRIPT), run_name="__main__")
