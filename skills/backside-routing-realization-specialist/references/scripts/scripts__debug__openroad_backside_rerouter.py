#!/usr/bin/env python3.11
"""OpenROAD/OpenDB-backed local rerouter for targeted net rewrites.

This is the first step toward "our own rerouter": we do not clone TritonRoute.
Instead, we build a minimal net-level wire rewrite engine on top of OpenDB
dbWire/dbWireEncoder. A separate heuristic layer can later generate route
specifications for this engine.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--def", dest="in_def", required=True, help="Input DEF.")
    p.add_argument("--out-def", required=True, help="Output patched DEF.")
    p.add_argument(
        "--techlef",
        required=True,
        help="Tech LEF used by OpenROAD.",
    )
    p.add_argument(
        "--celllef",
        required=True,
        help="Cell LEF used by OpenROAD.",
    )
    p.add_argument(
        "--route-spec",
        required=True,
        help="JSON route spec describing target net rewrite.",
    )
    p.add_argument(
        "--openroad-bin",
        default="external_tools/OpenROAD-flow-scripts/tools/OpenROAD/build/bin/openroad",
    )
    p.add_argument(
        "--sanitize-def",
        action="store_true",
        help="Sanitize Innovus DEF using sanitize_def_for_openroad.py before import.",
    )
    p.add_argument(
        "--emit-tcl-only",
        action="store_true",
        help="Only emit the generated Tcl script and do not run OpenROAD.",
    )
    p.add_argument(
        "--out-tcl",
        default="",
        help="Optional path to keep the generated Tcl script.",
    )
    return p.parse_args()


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=True,
    )


def tcl_quote(path: Path | str) -> str:
    return "{" + str(path) + "}"


def load_spec(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "net" not in data or "ops" not in data:
        raise SystemExit("route spec must contain 'net' and 'ops'")
    return data


def maybe_sanitize_def(root: Path, in_def: Path) -> Path:
    sanitized = Path(tempfile.mkstemp(prefix="openroad_sanitized_", suffix=".def")[1])
    run(
        [
            "python3.11",
            "scripts/debug/sanitize_def_for_openroad.py",
            "--in-def",
            str(in_def),
            "--out-def",
            str(sanitized),
        ],
        cwd=root,
    )
    return sanitized


def op_to_tcl(op: dict) -> str:
    kind = op["op"]
    if kind == "new_path":
        start = op["start"]
        if start == "ROOT":
            return f'$enc newPath $LAYER({op["layer"]}) "ROUTED"'
        return f'$enc newPath $J({start})'
    if kind == "add_point":
        x = op["x"]
        y = op["y"]
        ext = op.get("ext")
        assign = f'set J({op["name"]}) ' if "name" in op else ""
        if ext is None:
            return f"{assign}[$enc addPoint {x} {y}]" if assign else f"$enc addPoint {x} {y}"
        return f"{assign}[$enc addPoint {x} {y} {ext}]" if assign else f"$enc addPoint {x} {y} {ext}"
    if kind == "add_tech_via":
        assign = f'set J({op["name"]}) ' if "name" in op else ""
        return f'{assign}[$enc addTechVia $VIA({op["via"]})]' if assign else f'$enc addTechVia $VIA({op["via"]})'
    raise SystemExit(f"unsupported op kind: {kind}")


def build_tcl(in_def: Path, out_def: Path, techlef: Path, celllef: Path, spec: dict) -> str:
    layers = sorted({op["layer"] for op in spec["ops"] if op["op"] == "new_path" and op["start"] == "ROOT"})
    vias = sorted({op["via"] for op in spec["ops"] if op["op"] == "add_tech_via"})
    tcl: list[str] = []
    tcl.append(f"read_lef {tcl_quote(techlef)}")
    tcl.append(f"read_lef {tcl_quote(celllef)}")
    tcl.append(f"read_def {tcl_quote(in_def)}")
    tcl.append("set block [ord::get_db_block]")
    tcl.append(f'set net [$block findNet "{spec["net"]}"]')
    tcl.append('if {$net == "NULL" || $net == ""} { error "target net not found" }')
    tcl.append("set wire [$net getWire]")
    tcl.append('if {$wire != "NULL" && $wire != ""} { odb::dbWire_destroy $wire }')
    tcl.append("set wire [odb::dbWire_create $net]")
    tcl.append("set enc [odb::dbWireEncoder]")
    tcl.append("$enc begin $wire")
    for layer in layers:
        tcl.append(f'set LAYER({layer}) [[[$block getDataBase] getTech] findLayer "{layer}"]')
    for via in vias:
        tcl.append(f'set VIA({via}) [[[$block getDataBase] getTech] findVia "{via}"]')
        tcl.append(f'if {{$VIA({via}) == "NULL" || $VIA({via}) == ""}} {{ error "via {via} not found" }}')
    tcl.append("array set J {}")
    for op in spec["ops"]:
        tcl.append(op_to_tcl(op))
    tcl.append("$enc end")
    tcl.append("odb::dbNet_setWireOrdered $net 0")
    tcl.append(f"write_def {tcl_quote(out_def)}")
    tcl.append("exit")
    return "\n".join(tcl) + "\n"


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[2]
    in_def = Path(args.in_def)
    out_def = Path(args.out_def)
    techlef = Path(args.techlef)
    celllef = Path(args.celllef)
    spec_path = Path(args.route_spec)
    openroad = Path(args.openroad_bin)
    spec = load_spec(spec_path)

    if not in_def.is_absolute():
        in_def = (root / in_def).resolve()
    if not out_def.is_absolute():
        out_def = (root / out_def).resolve()
    if not techlef.is_absolute():
        techlef = (root / techlef).resolve()
    if not celllef.is_absolute():
        celllef = (root / celllef).resolve()
    if not spec_path.is_absolute():
        spec_path = (root / spec_path).resolve()
    if not openroad.is_absolute():
        openroad = (root / openroad).resolve()

    work_def = maybe_sanitize_def(root, in_def) if args.sanitize_def else in_def
    tcl = build_tcl(work_def, out_def, techlef, celllef, spec)

    if args.out_tcl:
        out_tcl = Path(args.out_tcl)
        if not out_tcl.is_absolute():
            out_tcl = (root / out_tcl).resolve()
        out_tcl.parent.mkdir(parents=True, exist_ok=True)
        out_tcl.write_text(tcl, encoding="utf-8")
    else:
        out_tcl = Path(tempfile.mkstemp(prefix="openroad_rerouter_", suffix=".tcl")[1])
        out_tcl.write_text(tcl, encoding="utf-8")

    print(f"route_spec={spec_path}")
    print(f"input_def={work_def}")
    print(f"output_def={out_def}")
    print(f"tcl={out_tcl}")

    if args.emit_tcl_only:
        return 0

    cp = run([str(openroad), str(out_tcl)], cwd=root)
    if cp.stdout:
        print(cp.stdout, end="")
    if cp.stderr:
        print(cp.stderr, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
