#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT"

DESIGN="${1:-systolic_array_8x8}"
RUN_TAG="${2:-gt3_route_rc_consistency_research_$(date +%Y%m%d_%H%M%S)}"
TASK_BRIEF="${TASK_BRIEF:-$ROOT/slurm_logs/04_delay_modeling/task_brief_backside_via_and_layer_policy_20260304.md}"
BACKSIDE_SIGNAL_NET_FILE="${BACKSIDE_SIGNAL_NET_FILE:-$ROOT/slurm_logs/04_delay_modeling/s8_top50_safe_signal_nets_20260304_0848.txt}"
BACKSIDE_SIGNAL_PATTERNS_FALLBACK="${BACKSIDE_SIGNAL_PATTERNS_FALLBACK:-c_out* valid_out valid_in *_checksum_*}"
BACKSIDE_SIGNAL_NET_BOTTOM_INDEX="${BACKSIDE_SIGNAL_NET_BOTTOM_INDEX:-1}"
BACKSIDE_SIGNAL_NET_TOP_INDEX="${BACKSIDE_SIGNAL_NET_TOP_INDEX:-2}"

bash "$ROOT/scripts/common/knowledge_gate.sh" \
  --scope "submit_gt3_route_rc_consistency" \
  --task-brief "$TASK_BRIEF"

PARTITION="${SLURM_PARTITION_OVERRIDE:-cpu-research}"
QOS="${SLURM_QOS_OVERRIDE:-olympus-cpu-research}"
CPUS="${SLURM_CPUS_OVERRIDE:-8}"
MEM="${SLURM_MEM_OVERRIDE:-64G}"
TIME_LIMIT="${SLURM_TIME_OVERRIDE:-06:00:00}"
FLOW_LOCAL_CPU="${FLOW_LOCAL_CPU:-$CPUS}"
FLOW_LOCAL_CPU_MAX="${FLOW_LOCAL_CPU_MAX:-8}"

if [[ ! "$CPUS" =~ ^[0-9]+$ || ! "$FLOW_LOCAL_CPU" =~ ^[0-9]+$ || ! "$FLOW_LOCAL_CPU_MAX" =~ ^[0-9]+$ ]]; then
  echo "ERROR: CPUS/FLOW_LOCAL_CPU/FLOW_LOCAL_CPU_MAX must be non-negative integers"
  exit 2
fi
if (( FLOW_LOCAL_CPU_MAX == 0 )); then
  echo "WARN: FLOW_LOCAL_CPU_MAX=0 disables flow-level local CPU override"
fi
if (( FLOW_LOCAL_CPU_MAX > 0 && FLOW_LOCAL_CPU > FLOW_LOCAL_CPU_MAX )); then
  echo "WARN: FLOW_LOCAL_CPU=$FLOW_LOCAL_CPU > FLOW_LOCAL_CPU_MAX=$FLOW_LOCAL_CPU_MAX; capping."
  FLOW_LOCAL_CPU="$FLOW_LOCAL_CPU_MAX"
fi
if (( FLOW_LOCAL_CPU > CPUS )); then
  echo "WARN: FLOW_LOCAL_CPU=$FLOW_LOCAL_CPU > CPUS=$CPUS; capping to CPUS."
  FLOW_LOCAL_CPU="$CPUS"
fi
FLOW_LOCAL_CPU_ARG=""
if (( FLOW_LOCAL_CPU > 0 )); then
  FLOW_LOCAL_CPU_ARG="--local-cpu=$FLOW_LOCAL_CPU"
fi

LOG_ROOT="$ROOT/slurm_logs/04_delay_modeling"
WRAPPER_DIR="$LOG_ROOT/wrappers/$RUN_TAG"
MON_PREFIX="$LOG_ROOT/${RUN_TAG}.monitor"
JOBS_TSV="$LOG_ROOT/${RUN_TAG}.jobs.tsv"

mkdir -p "$WRAPPER_DIR"

PLACE_WRAPPER="$WRAPPER_DIR/place_wrapper.sh"
cat > "$PLACE_WRAPPER" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
ROOT="__ROOT__"
DESIGN="__DESIGN__"
cd "$ROOT"

export GT3_FORCE_NO_CAP_TABLE=1
export GT3_USE_SIGNAL_BACKSIDE=1
export GT3_BACKSIDE_TECHLEF_MODE=ntsv_nominal

bash "$ROOT/scripts/stages/innovus/run.sh" "$DESIGN" \
  --BSPDN-HI \
  --tech-profile=gt3 \
  --from=floorplan \
  --to=place \
  --util=0.6 \
  --skip-prects-opt \
  --prects-mode=full \
  --signal-route-bottom-index=4 \
  --signal-route-top-index=13 \
  __FLOW_LOCAL_CPU_ARG__ \
  --auto-period-from-dc \
  --innovus-sdc-compat
EOF

sed -i "s|__ROOT__|$ROOT|g; s|__DESIGN__|$DESIGN|g; s|__FLOW_LOCAL_CPU_ARG__|$FLOW_LOCAL_CPU_ARG|g" "$PLACE_WRAPPER"
chmod +x "$PLACE_WRAPPER"

PLACE_OUT="$ROOT/slurm_logs/${RUN_TAG}_place_%j.out"
PLACE_ERR="$ROOT/slurm_logs/${RUN_TAG}_place_%j.err"
PLACE_JOBID=$(sbatch --parsable \
  --partition="$PARTITION" \
  --qos="$QOS" \
  --cpus-per-task="$CPUS" \
  --mem="$MEM" \
  --time="$TIME_LIMIT" \
  --job-name="${RUN_TAG}_place" \
  -o "$PLACE_OUT" \
  -e "$PLACE_ERR" \
  "$PLACE_WRAPPER")

PLACE_STDOUT_RESOLVED="$ROOT/slurm_logs/${RUN_TAG}_place_${PLACE_JOBID}.out"
PLACE_STDERR_RESOLVED="$ROOT/slurm_logs/${RUN_TAG}_place_${PLACE_JOBID}.err"

FRONT_WRAPPER="$WRAPPER_DIR/front_wrapper.sh"
cat > "$FRONT_WRAPPER" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
ROOT="__ROOT__"
DESIGN="__DESIGN__"
PLACE_STDOUT="__PLACE_STDOUT__"
cd "$ROOT"

OUT_DIR=$(awk -F'"' '/set OUT_DIR "/ {print $2; exit}' "$PLACE_STDOUT")
if [[ -z "${OUT_DIR:-}" ]] || [[ ! -d "$OUT_DIR" ]]; then
  echo "ERROR: failed to parse OUT_DIR from $PLACE_STDOUT"
  exit 2
fi

RESUME_DEF="$OUT_DIR/${DESIGN}.placed.def"
RESUME_V="$OUT_DIR/${DESIGN}.placed.v"
RESUME_SDC="$OUT_DIR/${DESIGN}.innovus_compat.sdc"
for f in "$RESUME_DEF" "$RESUME_V" "$RESUME_SDC"; do
  if [[ ! -f "$f" ]]; then
    echo "ERROR: missing resume artifact: $f"
    exit 3
  fi
done

export GT3_FORCE_NO_CAP_TABLE=1
export GT3_USE_SIGNAL_BACKSIDE=1
export GT3_BACKSIDE_TECHLEF_MODE=ntsv_nominal

bash "$ROOT/scripts/stages/innovus/run.sh" "$DESIGN" \
  --tech-profile=gt3 \
  --from=cts \
  --to=route \
  --cts-backside \
  --cts-route-bottom=M4 \
  --cts-route-top=M5 \
  --cts-no-route-autotrim \
  --resume-def="$RESUME_DEF" \
  --netlist="$RESUME_V" \
  --sdc="$RESUME_SDC" \
  --util=0.6 \
  --skip-prects-opt \
  --prects-mode=full \
  --signal-route-bottom-index=4 \
  --signal-route-top-index=13 \
  __FLOW_LOCAL_CPU_ARG__ \
  --auto-period-from-dc \
  --innovus-sdc-compat
EOF

sed -i "s|__ROOT__|$ROOT|g; s|__DESIGN__|$DESIGN|g; s|__PLACE_STDOUT__|$PLACE_STDOUT_RESOLVED|g; s|__FLOW_LOCAL_CPU_ARG__|$FLOW_LOCAL_CPU_ARG|g" "$FRONT_WRAPPER"
chmod +x "$FRONT_WRAPPER"

BACK_WRAPPER="$WRAPPER_DIR/back_wrapper.sh"
cat > "$BACK_WRAPPER" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
ROOT="__ROOT__"
DESIGN="__DESIGN__"
PLACE_STDOUT="__PLACE_STDOUT__"
SIG_NET_FILE="__SIG_NET_FILE__"
SIG_PAT_FALLBACK="__SIG_PAT_FALLBACK__"
cd "$ROOT"

OUT_DIR=$(awk -F'"' '/set OUT_DIR "/ {print $2; exit}' "$PLACE_STDOUT")
if [[ -z "${OUT_DIR:-}" ]] || [[ ! -d "$OUT_DIR" ]]; then
  echo "ERROR: failed to parse OUT_DIR from $PLACE_STDOUT"
  exit 2
fi

RESUME_DEF="$OUT_DIR/${DESIGN}.placed.def"
RESUME_V="$OUT_DIR/${DESIGN}.placed.v"
RESUME_SDC="$OUT_DIR/${DESIGN}.innovus_compat.sdc"
for f in "$RESUME_DEF" "$RESUME_V" "$RESUME_SDC"; do
  if [[ ! -f "$f" ]]; then
    echo "ERROR: missing resume artifact: $f"
    exit 3
  fi
done

export GT3_FORCE_NO_CAP_TABLE=1
export GT3_USE_SIGNAL_BACKSIDE=1
export GT3_BACKSIDE_TECHLEF_MODE=ntsv_nominal

ROUTE_BACKSIDE_NETS_ARG="$SIG_PAT_FALLBACK"
if [[ -f "$SIG_NET_FILE" ]]; then
  mapfile -t _sig_nets < <(grep -v '^[[:space:]]*$' "$SIG_NET_FILE" | head -n 200)
  if (( ${#_sig_nets[@]} > 0 )); then
    ROUTE_BACKSIDE_NETS_ARG="${_sig_nets[*]}"
  fi
fi
echo "[submit-rc-consistency] signal backside nets source: $SIG_NET_FILE"
echo "[submit-rc-consistency] signal backside patterns: $ROUTE_BACKSIDE_NETS_ARG"
echo "[submit-rc-consistency] signal backside layer window index: __BS_NET_BOT__..__BS_NET_TOP__"

bash "$ROOT/scripts/stages/innovus/run.sh" "$DESIGN" \
  --tech-profile=gt3 \
  --from=cts \
  --to=route \
  --cts-backside \
  --cts-route-bottom=M4 \
  --cts-route-top=M5 \
  --cts-no-route-autotrim \
  --resume-def="$RESUME_DEF" \
  --netlist="$RESUME_V" \
  --sdc="$RESUME_SDC" \
  --util=0.6 \
  --skip-prects-opt \
  --prects-mode=full \
  --open-backside-route \
  --route-backside-nets="$ROUTE_BACKSIDE_NETS_ARG" \
  --route-backside-net-bottom-index=__BS_NET_BOT__ \
  --route-backside-net-top-index=__BS_NET_TOP__ \
  --no-route-backside-expand-clock-tree \
  __FLOW_LOCAL_CPU_ARG__ \
  --auto-period-from-dc \
  --innovus-sdc-compat
EOF

sed -i "s|__ROOT__|$ROOT|g; s|__DESIGN__|$DESIGN|g; s|__PLACE_STDOUT__|$PLACE_STDOUT_RESOLVED|g; s|__SIG_NET_FILE__|$BACKSIDE_SIGNAL_NET_FILE|g; s|__SIG_PAT_FALLBACK__|$BACKSIDE_SIGNAL_PATTERNS_FALLBACK|g; s|__BS_NET_BOT__|$BACKSIDE_SIGNAL_NET_BOTTOM_INDEX|g; s|__BS_NET_TOP__|$BACKSIDE_SIGNAL_NET_TOP_INDEX|g; s|__FLOW_LOCAL_CPU_ARG__|$FLOW_LOCAL_CPU_ARG|g" "$BACK_WRAPPER"
chmod +x "$BACK_WRAPPER"

FRONT_OUT="$ROOT/slurm_logs/${RUN_TAG}_front_%j.out"
FRONT_ERR="$ROOT/slurm_logs/${RUN_TAG}_front_%j.err"
BACK_OUT="$ROOT/slurm_logs/${RUN_TAG}_back_%j.out"
BACK_ERR="$ROOT/slurm_logs/${RUN_TAG}_back_%j.err"

FRONT_JOBID=$(sbatch --parsable \
  --partition="$PARTITION" \
  --qos="$QOS" \
  --cpus-per-task="$CPUS" \
  --mem="$MEM" \
  --time="$TIME_LIMIT" \
  --dependency=afterok:"$PLACE_JOBID" \
  --job-name="${RUN_TAG}_front" \
  -o "$FRONT_OUT" \
  -e "$FRONT_ERR" \
  "$FRONT_WRAPPER")

BACK_JOBID=$(sbatch --parsable \
  --partition="$PARTITION" \
  --qos="$QOS" \
  --cpus-per-task="$CPUS" \
  --mem="$MEM" \
  --time="$TIME_LIMIT" \
  --dependency=afterok:"$PLACE_JOBID" \
  --job-name="${RUN_TAG}_back" \
  -o "$BACK_OUT" \
  -e "$BACK_ERR" \
  "$BACK_WRAPPER")

cat > "$JOBS_TSV" <<EOF
phase	mode	job_id	dep	stdout	stderr	wrapper
place	prep_place	$PLACE_JOBID	-	$ROOT/slurm_logs/${RUN_TAG}_place_${PLACE_JOBID}.out	$ROOT/slurm_logs/${RUN_TAG}_place_${PLACE_JOBID}.err	$PLACE_WRAPPER
cts_route	frontside	$FRONT_JOBID	$PLACE_JOBID	$ROOT/slurm_logs/${RUN_TAG}_front_${FRONT_JOBID}.out	$ROOT/slurm_logs/${RUN_TAG}_front_${FRONT_JOBID}.err	$FRONT_WRAPPER
cts_route	backside_open	$BACK_JOBID	$PLACE_JOBID	$ROOT/slurm_logs/${RUN_TAG}_back_${BACK_JOBID}.out	$ROOT/slurm_logs/${RUN_TAG}_back_${BACK_JOBID}.err	$BACK_WRAPPER
EOF

MON_LOG="${MON_PREFIX}.log"
MON_PID="${MON_PREFIX}.pid"

MON_JOBID=$(sbatch --parsable \
  --partition="$PARTITION" \
  --qos="$QOS" \
  --cpus-per-task=1 \
  --mem=1G \
  --time="$TIME_LIMIT" \
  --job-name="${RUN_TAG}_monitor" \
  -o "$MON_LOG" \
  -e "$MON_LOG" \
  --wrap "cd '$ROOT' && python3 '$ROOT/scripts/debug/progress_monitor.py' --manifest '$JOBS_TSV' --out-prefix '$MON_PREFIX' --interval 20 --exit-when-complete")
echo "$MON_JOBID" > "$MON_PID"

cat <<EOF
run_tag=$RUN_TAG
jobs_tsv=$JOBS_TSV
monitor_md=${MON_PREFIX}.md
monitor_html=${MON_PREFIX}.html
monitor_history=${MON_PREFIX}.history.tsv
monitor_jobid_file=$MON_PID
monitor_jobid=$MON_JOBID
jobs: place=$PLACE_JOBID front=$FRONT_JOBID back=$BACK_JOBID
EOF
