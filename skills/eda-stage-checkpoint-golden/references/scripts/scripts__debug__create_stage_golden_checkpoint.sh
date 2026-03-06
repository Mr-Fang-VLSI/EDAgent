#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT"

usage() {
  cat <<'EOF'
Usage:
  scripts/debug/create_stage_golden_checkpoint.sh \
    --design=<design> \
    --tag=<golden_tag> \
    [--run-dir=<common_run_dir>] \
    [--place-run-dir=<run_dir>] \
    [--cts-run-dir=<run_dir>] \
    [--route-run-dir=<run_dir>] \
    [--tech-profile=<name>] \
    [--out-root=<path>]

Notes:
  - You can provide one common --run-dir, or per-stage run dirs.
  - Stage artifacts are copied (not symlinked) for immutability.
  - Expected files:
      place: <design>.placed.def,  <design>.placed.v,  <design>.innovus_compat.sdc
      cts:   <design>.postcts.def, <design>.postcts.v, <design>.innovus_compat.sdc
      route: <design>.routed.def,  <design>.routed.v,  <design>.innovus_compat.sdc
EOF
}

DESIGN=""
TAG=""
COMMON_RUN_DIR=""
PLACE_RUN_DIR=""
CTS_RUN_DIR=""
ROUTE_RUN_DIR=""
TECH_PROFILE="${TECH_PROFILE:-gt3}"
OUT_ROOT="${OUT_ROOT:-$ROOT/regression/stage_checkpoints}"

for arg in "$@"; do
  case "$arg" in
    --design=*) DESIGN="${arg#--design=}" ;;
    --tag=*) TAG="${arg#--tag=}" ;;
    --run-dir=*) COMMON_RUN_DIR="${arg#--run-dir=}" ;;
    --place-run-dir=*) PLACE_RUN_DIR="${arg#--place-run-dir=}" ;;
    --cts-run-dir=*) CTS_RUN_DIR="${arg#--cts-run-dir=}" ;;
    --route-run-dir=*) ROUTE_RUN_DIR="${arg#--route-run-dir=}" ;;
    --tech-profile=*) TECH_PROFILE="${arg#--tech-profile=}" ;;
    --out-root=*) OUT_ROOT="${arg#--out-root=}" ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "ERROR: unknown arg: $arg" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ -z "$DESIGN" || -z "$TAG" ]]; then
  echo "ERROR: --design and --tag are required" >&2
  usage
  exit 2
fi

if [[ -n "$COMMON_RUN_DIR" ]]; then
  [[ -z "$PLACE_RUN_DIR" ]] && PLACE_RUN_DIR="$COMMON_RUN_DIR"
  [[ -z "$CTS_RUN_DIR" ]] && CTS_RUN_DIR="$COMMON_RUN_DIR"
  [[ -z "$ROUTE_RUN_DIR" ]] && ROUTE_RUN_DIR="$COMMON_RUN_DIR"
fi

BUNDLE_DIR="$OUT_ROOT/$TAG/$DESIGN"
mkdir -p "$BUNDLE_DIR"

MANIFEST_TSV="$BUNDLE_DIR/manifest.tsv"
MANIFEST_MD="$BUNDLE_DIR/manifest.md"
SHA_TSV="$BUNDLE_DIR/sha256.tsv"
RESTORE_SH="$BUNDLE_DIR/restore_examples.sh"

tmp_sha=$(mktemp)
trap 'rm -f "$tmp_sha"' EXIT

copy_stage() {
  local stage="$1"
  local run_dir="$2"
  local def_suffix="$3"
  local v_suffix="$4"

  local stage_dir="$BUNDLE_DIR/$stage"
  mkdir -p "$stage_dir"

  if [[ -z "$run_dir" ]]; then
    echo -e "$stage\tMISSING\tMISSING\tMISSING\tMISSING\tMISSING\tMISSING"
    return 0
  fi

  if [[ ! -d "$run_dir" ]]; then
    echo "ERROR: $stage run dir not found: $run_dir" >&2
    exit 3
  fi

  local def_src="$run_dir/${DESIGN}.${def_suffix}.def"
  local v_src="$run_dir/${DESIGN}.${v_suffix}.v"
  local sdc_src="$run_dir/${DESIGN}.innovus_compat.sdc"
  local auto_sdc_src="$run_dir/${DESIGN}.auto_period.sdc"

  if [[ ! -f "$def_src" ]]; then
    echo "ERROR: missing $stage def: $def_src" >&2
    exit 4
  fi
  if [[ ! -f "$v_src" ]]; then
    echo "ERROR: missing $stage netlist: $v_src" >&2
    exit 5
  fi
  if [[ ! -f "$sdc_src" ]]; then
    if [[ -f "$auto_sdc_src" ]]; then
      sdc_src="$auto_sdc_src"
    else
      echo "ERROR: missing $stage sdc: $run_dir/${DESIGN}.innovus_compat.sdc" >&2
      exit 6
    fi
  fi

  local def_dst="$stage_dir/${DESIGN}.${stage}.def"
  local v_dst="$stage_dir/${DESIGN}.${stage}.v"
  local sdc_dst="$stage_dir/${DESIGN}.${stage}.sdc"

  cp -f "$def_src" "$def_dst"
  cp -f "$v_src" "$v_dst"
  cp -f "$sdc_src" "$sdc_dst"

  sha256sum "$def_dst" "$v_dst" "$sdc_dst" >> "$tmp_sha"

  echo -e "$stage\tOK\t$run_dir\t$def_dst\t$v_dst\t$sdc_dst\t$TECH_PROFILE"
}

{
  echo -e "stage\tstatus\tsource_run_dir\tdef\tnetlist\tsdc\ttech_profile"
  copy_stage "place" "$PLACE_RUN_DIR" "placed" "placed"
  copy_stage "cts" "$CTS_RUN_DIR" "postcts" "postcts"
  copy_stage "route" "$ROUTE_RUN_DIR" "routed" "routed"
} > "$MANIFEST_TSV"

{
  echo -e "sha256\tfile"
  awk '{print $1 "\t" $2}' "$tmp_sha"
} > "$SHA_TSV"

cat > "$RESTORE_SH" <<EOF
#!/usr/bin/env bash
set -euo pipefail

# Example resume commands from golden checkpoints.
ROOT="\$(cd "\$(dirname "\$0")/../../../.." && pwd)"
DESIGN="$DESIGN"

# from place -> cts
bash "\$ROOT/scripts/stages/innovus/run.sh" "\$DESIGN" \\
  --tech-profile="$TECH_PROFILE" \\
  --from=cts --to=cts \\
  --resume-def="$BUNDLE_DIR/place/${DESIGN}.place.def" \\
  --netlist="$BUNDLE_DIR/place/${DESIGN}.place.v" \\
  --sdc="$BUNDLE_DIR/place/${DESIGN}.place.sdc"

# from cts -> route
bash "\$ROOT/scripts/stages/innovus/run.sh" "\$DESIGN" \\
  --tech-profile="$TECH_PROFILE" \\
  --from=route --to=route \\
  --resume-def="$BUNDLE_DIR/cts/${DESIGN}.cts.def" \\
  --netlist="$BUNDLE_DIR/cts/${DESIGN}.cts.v" \\
  --sdc="$BUNDLE_DIR/cts/${DESIGN}.cts.sdc"

# from route -> extract/reports
bash "\$ROOT/scripts/stages/innovus/run.sh" "\$DESIGN" \\
  --tech-profile="$TECH_PROFILE" \\
  --from=extract --to=reports \\
  --resume-def="$BUNDLE_DIR/route/${DESIGN}.route.def" \\
  --netlist="$BUNDLE_DIR/route/${DESIGN}.route.v" \\
  --sdc="$BUNDLE_DIR/route/${DESIGN}.route.sdc"
EOF

chmod +x "$RESTORE_SH"

{
  echo "# Stage Golden Checkpoint"
  echo
  echo "- design: \`$DESIGN\`"
  echo "- tag: \`$TAG\`"
  echo "- bundle_dir: \`$BUNDLE_DIR\`"
  echo "- created_at: \`$(date '+%Y-%m-%d %H:%M:%S')\`"
  echo "- tech_profile: \`$TECH_PROFILE\`"
  echo
  echo "## Stage Manifest"
  echo
  echo "| stage | status | source_run_dir | def | netlist | sdc |"
  echo "|---|---|---|---|---|---|"
  awk -F'\t' 'NR>1 {printf "| %s | %s | `%s` | `%s` | `%s` | `%s` |\n",$1,$2,$3,$4,$5,$6}' "$MANIFEST_TSV"
  echo
  echo "## Files"
  echo
  echo "- manifest: \`$MANIFEST_TSV\`"
  echo "- checksums: \`$SHA_TSV\`"
  echo "- restore examples: \`$RESTORE_SH\`"
} > "$MANIFEST_MD"

echo "golden_bundle=$BUNDLE_DIR"
echo "manifest_tsv=$MANIFEST_TSV"
echo "manifest_md=$MANIFEST_MD"
echo "sha_tsv=$SHA_TSV"
echo "restore_examples=$RESTORE_SH"
