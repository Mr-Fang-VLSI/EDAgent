#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

TASK_BRIEF=""
SCOPE="unknown_scope"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-brief)
      TASK_BRIEF="${2:-}"
      shift 2
      ;;
    --scope)
      SCOPE="${2:-unknown_scope}"
      shift 2
      ;;
    *)
      echo "[knowledge-gate] ERROR: unknown arg: $1"
      exit 2
      ;;
  esac
done

err() {
  echo "[knowledge-gate] FAIL: $1" >&2
  exit 1
}

req_file() {
  local f="$1"
  [[ -f "$f" ]] || err "missing required file: $f"
}

req_file "$ROOT/docs/knowledge_base/00_START_HERE.md"
req_file "$ROOT/docs/knowledge_base/10_TASK_EXECUTION_PROTOCOL.md"
req_file "$ROOT/docs/knowledge_base/11_INTERACTION_CHECKLIST.md"
req_file "$ROOT/docs/tool_registry/README.md"
req_file "$ROOT/docs/tool_registry/tool_catalog.tsv"
req_file "$ROOT/slurm_logs/00_meta/knowledge_tool_maintenance_log.md"
req_file "$ROOT/AGENTS.md"
req_file "$ROOT/skills/00_SKILL_SYSTEM_MANIFEST.tsv"
req_file "$ROOT/scripts/common/skill_system_audit.py"
req_file "$ROOT/scripts/common/infra_stack_guard.py"
req_file "$ROOT/scripts/common/init_research_chain.py"
req_file "$ROOT/scripts/common/research_chain_guard.py"

if [[ -z "$TASK_BRIEF" ]]; then
  err "--task-brief is required"
fi
[[ -f "$TASK_BRIEF" ]] || err "task brief not found: $TASK_BRIEF"

# Lightweight quality checks on task brief.
grep -q "## 3. Mandatory reading" "$TASK_BRIEF" || err "task brief missing 'Mandatory reading' section: $TASK_BRIEF"
grep -Eq '^\s*-\s*\[x\]\s*`docs/knowledge_base/00_START_HERE\.md`' "$TASK_BRIEF" || err "task brief must mark 00_START_HERE as read: $TASK_BRIEF"
grep -Eq '^\s*-\s*\[x\]\s*`docs/knowledge_base/10_TASK_EXECUTION_PROTOCOL\.md`' "$TASK_BRIEF" || err "task brief must mark 10_TASK_EXECUTION_PROTOCOL as read: $TASK_BRIEF"

# Ensure maintenance log has today's entry.
TODAY="$(date +%Y-%m-%d)"
if ! grep -q "$TODAY" "$ROOT/slurm_logs/00_meta/knowledge_tool_maintenance_log.md"; then
  err "maintenance log has no entry for today ($TODAY): slurm_logs/00_meta/knowledge_tool_maintenance_log.md"
fi

if ! grep -q "tool_catalog query" "$ROOT/slurm_logs/00_meta/knowledge_tool_maintenance_log.md"; then
  err "maintenance log does not show tool_catalog query evidence"
fi

echo "[knowledge-gate] PASS scope=$SCOPE task_brief=$TASK_BRIEF"
