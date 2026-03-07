#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
BIN="$ROOT/scripts/debug/backside_net_scorer"
BUILD="$ROOT/scripts/debug/build_backside_net_scorer.sh"

DEF_FILE=""
OUT_PREFIX=""
TOPK=64
REPORT_TOPN=2000
CAP_RATIO=0.08
CAP_DBU=0
MIN_LEN=1000
CRIT_FILE=""
CRIT_TYPE="criticality"
MODEL_MODE="route"
SOLVER_MODE="lagrangian_swap"
SELECTION_MODE="hybrid"
LAGRANGIAN_ITERS=24
KNAPSACK_WEIGHT_SCALE_DBU=2000
SWAP_ROUNDS=40
SWAP_SCAN_SELECTED=256
SWAP_SCAN_UNSELECTED=1024
MAX_NET_CAP_FRAC=0.25
RESERVE_CLOCK_CAP_RATIO=0.0
MIN_SCORE=0.0
TECHLEF_FILE="$ROOT/tech/ASAP7/techlef_misc/asap7_tech_4x_170803_mg0005.lef"
ENABLE_PDK_TIMING=1
W_PDK_TIMING=0.90
W_PDK_GAIN=""
W_PDK_DELTA_R=""
W_PDK_DELTA_C=""
W_PDK_VIA_PROXY=""
BACKSIDE_BIAS_EXP=0.60
LOW_LAYERS="M1,M2,M3"
BACKSIDE_LAYERS="BPR,BM1,BM2"
W_PIN_DENSITY=0.30
W_NET_DENSITY=0.25
W_VIA=0.25
W_CLOCK_PROXIMITY=0.35
DENSITY_BIN_DBU=20000
ANALYTICAL_STEINER_ALPHA=0.15
INCLUDE_CLOCK=0
INCLUDE_CONTROL=0
W_CLOCK=""
W_CRITICAL=""
W_CONTROL=""
W_LENGTH=""
W_LOW_METAL=""
W_HPWL=""
W_FANOUT=""

for arg in "$@"; do
  case "$arg" in
    --def-file=*) DEF_FILE="${arg#--def-file=}" ;;
    --out-prefix=*) OUT_PREFIX="${arg#--out-prefix=}" ;;
    --topk=*) TOPK="${arg#--topk=}" ;;
    --report-topn=*) REPORT_TOPN="${arg#--report-topn=}" ;;
    --capacity-ratio=*) CAP_RATIO="${arg#--capacity-ratio=}" ;;
    --capacity-dbu=*) CAP_DBU="${arg#--capacity-dbu=}" ;;
    --min-length-dbu=*) MIN_LEN="${arg#--min-length-dbu=}" ;;
    --criticality-file=*) CRIT_FILE="${arg#--criticality-file=}" ;;
    --criticality-type=*) CRIT_TYPE="${arg#--criticality-type=}" ;;
    --model-mode=*) MODEL_MODE="${arg#--model-mode=}" ;;
    --solver-mode=*) SOLVER_MODE="${arg#--solver-mode=}" ;;
    --selection-mode=*) SELECTION_MODE="${arg#--selection-mode=}" ;;
    --lagrangian-iters=*) LAGRANGIAN_ITERS="${arg#--lagrangian-iters=}" ;;
    --knapsack-weight-scale-dbu=*) KNAPSACK_WEIGHT_SCALE_DBU="${arg#--knapsack-weight-scale-dbu=}" ;;
    --swap-rounds=*) SWAP_ROUNDS="${arg#--swap-rounds=}" ;;
    --swap-scan-selected=*) SWAP_SCAN_SELECTED="${arg#--swap-scan-selected=}" ;;
    --swap-scan-unselected=*) SWAP_SCAN_UNSELECTED="${arg#--swap-scan-unselected=}" ;;
    --max-net-capacity-frac=*) MAX_NET_CAP_FRAC="${arg#--max-net-capacity-frac=}" ;;
    --reserve-clock-capacity-ratio=*) RESERVE_CLOCK_CAP_RATIO="${arg#--reserve-clock-capacity-ratio=}" ;;
    --min-score=*) MIN_SCORE="${arg#--min-score=}" ;;
    --techlef-file=*) TECHLEF_FILE="${arg#--techlef-file=}" ;;
    --enable-pdk-timing=*) ENABLE_PDK_TIMING="${arg#--enable-pdk-timing=}" ;;
    --w-pdk-timing=*) W_PDK_TIMING="${arg#--w-pdk-timing=}" ;;
    --w-pdk-gain=*) W_PDK_GAIN="${arg#--w-pdk-gain=}" ;;
    --w-pdk-delta-r=*) W_PDK_DELTA_R="${arg#--w-pdk-delta-r=}" ;;
    --w-pdk-delta-c=*) W_PDK_DELTA_C="${arg#--w-pdk-delta-c=}" ;;
    --w-pdk-via-proxy=*) W_PDK_VIA_PROXY="${arg#--w-pdk-via-proxy=}" ;;
    --backside-bias-exp=*) BACKSIDE_BIAS_EXP="${arg#--backside-bias-exp=}" ;;
    --low-layers=*) LOW_LAYERS="${arg#--low-layers=}" ;;
    --backside-layers=*) BACKSIDE_LAYERS="${arg#--backside-layers=}" ;;
    --w-pin-density=*) W_PIN_DENSITY="${arg#--w-pin-density=}" ;;
    --w-net-density=*) W_NET_DENSITY="${arg#--w-net-density=}" ;;
    --w-via=*) W_VIA="${arg#--w-via=}" ;;
    --w-clock-proximity=*) W_CLOCK_PROXIMITY="${arg#--w-clock-proximity=}" ;;
    --density-bin-dbu=*) DENSITY_BIN_DBU="${arg#--density-bin-dbu=}" ;;
    --analytical-steiner-alpha=*) ANALYTICAL_STEINER_ALPHA="${arg#--analytical-steiner-alpha=}" ;;
    --include-clock) INCLUDE_CLOCK=1 ;;
    --include-control) INCLUDE_CONTROL=1 ;;
    --w-clock=*) W_CLOCK="${arg#--w-clock=}" ;;
    --w-critical=*) W_CRITICAL="${arg#--w-critical=}" ;;
    --w-control=*) W_CONTROL="${arg#--w-control=}" ;;
    --w-length=*) W_LENGTH="${arg#--w-length=}" ;;
    --w-low-metal=*) W_LOW_METAL="${arg#--w-low-metal=}" ;;
    --w-hpwl=*) W_HPWL="${arg#--w-hpwl=}" ;;
    --w-fanout=*) W_FANOUT="${arg#--w-fanout=}" ;;
    *)
      echo "ERROR: unknown arg: $arg"
      exit 1
      ;;
  esac
done

if [[ -z "$DEF_FILE" ]]; then
  echo "ERROR: --def-file is required"
  exit 1
fi
if [[ -z "$OUT_PREFIX" ]]; then
  ts=$(date +%Y%m%d_%H%M%S)
  OUT_PREFIX="$ROOT/slurm_logs/backside_cpp_select_${ts}"
fi

if [[ ! -x "$BIN" ]]; then
  "$BUILD"
fi

mkdir -p "$(dirname "$OUT_PREFIX")"
OUT_NETS="${OUT_PREFIX}.nets.txt"
OUT_REPORT="${OUT_PREFIX}.report.tsv"

cmd=(
  "$BIN"
  "--def-file=$DEF_FILE"
  "--out-nets=$OUT_NETS"
  "--out-report=$OUT_REPORT"
  "--topk=$TOPK"
  "--report-topn=$REPORT_TOPN"
  "--min-length-dbu=$MIN_LEN"
  "--min-score=$MIN_SCORE"
  "--criticality-type=$CRIT_TYPE"
  "--model-mode=$MODEL_MODE"
  "--solver-mode=$SOLVER_MODE"
  "--selection-mode=$SELECTION_MODE"
  "--lagrangian-iters=$LAGRANGIAN_ITERS"
  "--knapsack-weight-scale-dbu=$KNAPSACK_WEIGHT_SCALE_DBU"
  "--swap-rounds=$SWAP_ROUNDS"
  "--swap-scan-selected=$SWAP_SCAN_SELECTED"
  "--swap-scan-unselected=$SWAP_SCAN_UNSELECTED"
  "--max-net-capacity-frac=$MAX_NET_CAP_FRAC"
  "--reserve-clock-capacity-ratio=$RESERVE_CLOCK_CAP_RATIO"
  "--enable-pdk-timing=$ENABLE_PDK_TIMING"
  "--w-pdk-timing=$W_PDK_TIMING"
  "--backside-bias-exp=$BACKSIDE_BIAS_EXP"
  "--low-layers=$LOW_LAYERS"
  "--backside-layers=$BACKSIDE_LAYERS"
  "--w-pin-density=$W_PIN_DENSITY"
  "--w-net-density=$W_NET_DENSITY"
  "--w-via=$W_VIA"
  "--w-clock-proximity=$W_CLOCK_PROXIMITY"
  "--density-bin-dbu=$DENSITY_BIN_DBU"
  "--analytical-steiner-alpha=$ANALYTICAL_STEINER_ALPHA"
)

if [[ -n "$TECHLEF_FILE" ]]; then
  cmd+=("--techlef-file=$TECHLEF_FILE")
fi

if [[ "$CAP_DBU" -gt 0 ]]; then
  cmd+=("--capacity-dbu=$CAP_DBU")
else
  cmd+=("--capacity-ratio=$CAP_RATIO")
fi

if [[ -n "$CRIT_FILE" ]]; then
  cmd+=("--criticality-file=$CRIT_FILE")
fi
if [[ "$INCLUDE_CLOCK" -eq 1 ]]; then
  cmd+=("--include-clock")
fi
if [[ "$INCLUDE_CONTROL" -eq 1 ]]; then
  cmd+=("--include-control")
fi
if [[ -n "$W_PDK_GAIN" ]]; then
  cmd+=("--w-pdk-gain=$W_PDK_GAIN")
fi
if [[ -n "$W_PDK_DELTA_R" ]]; then
  cmd+=("--w-pdk-delta-r=$W_PDK_DELTA_R")
fi
if [[ -n "$W_PDK_DELTA_C" ]]; then
  cmd+=("--w-pdk-delta-c=$W_PDK_DELTA_C")
fi
if [[ -n "$W_PDK_VIA_PROXY" ]]; then
  cmd+=("--w-pdk-via-proxy=$W_PDK_VIA_PROXY")
fi
if [[ -n "$W_CLOCK" ]]; then
  cmd+=("--w-clock=$W_CLOCK")
fi
if [[ -n "$W_CRITICAL" ]]; then
  cmd+=("--w-critical=$W_CRITICAL")
fi
if [[ -n "$W_CONTROL" ]]; then
  cmd+=("--w-control=$W_CONTROL")
fi
if [[ -n "$W_LENGTH" ]]; then
  cmd+=("--w-length=$W_LENGTH")
fi
if [[ -n "$W_LOW_METAL" ]]; then
  cmd+=("--w-low-metal=$W_LOW_METAL")
fi
if [[ -n "$W_HPWL" ]]; then
  cmd+=("--w-hpwl=$W_HPWL")
fi
if [[ -n "$W_FANOUT" ]]; then
  cmd+=("--w-fanout=$W_FANOUT")
fi

echo "[select] running:"
printf '  %q' "${cmd[@]}"
echo
"${cmd[@]}"

echo "[select] out_nets   : $OUT_NETS"
echo "[select] out_report : $OUT_REPORT"
echo "[select] selected_count: $(wc -l < "$OUT_NETS" | awk '{print $1}')"
echo "[select] route-backside-nets arg preview:"
preview="$(tr '\n' ' ' < "$OUT_NETS")"
echo "${preview:0:200}"
