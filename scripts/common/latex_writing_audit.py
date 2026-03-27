#!/usr/bin/env python3
"""Audit active LaTeX writing assets and common manuscript risks.

Checks:
- active TeX closure from main.tex via \\include/\\input
- active bibliography files from \\bibliography
- case mismatches between \\includegraphics paths and on-disk files
- warning summary from main.log
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

INCLUDE_RE = re.compile(r"^(?!\s*%).*\\(?:include|input)\{([^}]+)\}", re.M)
GRAPHICS_RE = re.compile(
    r"^(?!\s*%).*\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", re.M
)
BIB_RE = re.compile(r"^(?!\s*%).*\\bibliography\{([^}]+)\}", re.M)


def resolve_tex(root: Path, ref: str) -> Path:
    path = root / ref
    if path.suffix != ".tex":
        path = path.with_suffix(".tex")
    return path


def walk_active_tex(root: Path, entry: Path) -> tuple[list[Path], set[str], set[str]]:
    visited: set[Path] = set()
    tex_files: list[Path] = []
    graphics: set[str] = set()
    bibs: set[str] = set()

    def walk(path: Path) -> None:
        path = path.resolve()
        if path in visited or not path.exists():
            return
        visited.add(path)
        tex_files.append(path)
        text = path.read_text(errors="ignore")

        for m in GRAPHICS_RE.finditer(text):
            graphics.add(m.group(1).lstrip("./"))

        for m in BIB_RE.finditer(text):
            for ref in m.group(1).split(","):
                ref = ref.strip()
                if not ref:
                    continue
                if not ref.endswith(".bib"):
                    ref += ".bib"
                bibs.add(ref)

        for m in INCLUDE_RE.finditer(text):
            walk(resolve_tex(root, m.group(1)))

    walk(entry)
    return tex_files, graphics, bibs


def collect_real_files(root: Path) -> dict[str, str]:
    real: dict[str, str] = {}
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            real[rel.lower()] = rel
    return real


def find_graphics_case_mismatches(root: Path, tex_files: list[Path]) -> list[str]:
    real_files = collect_real_files(root)
    mismatches: list[str] = []
    for tex in tex_files:
        text = tex.read_text(errors="ignore")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in GRAPHICS_RE.finditer(line):
                ref = m.group(1).lstrip("./")
                actual = real_files.get(ref.lower())
                if actual and actual != ref:
                    rel = tex.relative_to(root).as_posix()
                    mismatches.append(f"{rel}:{lineno}: {ref} -> {actual}")
    return mismatches


def parse_log_warnings(root: Path) -> list[str]:
    log = root / "main.log"
    if not log.exists():
        return ["main.log not found"]
    out: list[str] = []
    for lineno, line in enumerate(log.read_text(errors="ignore").splitlines(), start=1):
        if any(
            key in line
            for key in ("Warning", "Underfull", "Overfull", "undefined", "multiply defined")
        ):
            out.append(f"{lineno}: {line.strip()}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="LaTeX project root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    entry = root / "main.tex"
    if not entry.exists():
        raise SystemExit(f"main.tex not found under {root}")

    tex_files, graphics, bibs = walk_active_tex(root, entry)
    mismatches = find_graphics_case_mismatches(root, tex_files)
    warnings = parse_log_warnings(root)

    print("== Active TeX Files ==")
    for path in tex_files:
        print(path.relative_to(root).as_posix())

    print("\n== Active Bibliography Files ==")
    for bib in sorted(bibs):
        print(bib)

    print("\n== Active Graphics ==")
    for graphic in sorted(graphics):
        print(graphic)

    print("\n== Graphics Case Mismatches ==")
    if mismatches:
        for item in mismatches:
            print(item)
    else:
        print("None")

    print("\n== Log Warnings ==")
    if warnings:
        for item in warnings:
            print(item)
    else:
        print("None")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
