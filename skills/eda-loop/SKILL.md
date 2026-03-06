---
name: eda-loop
description: "Execute one scoped EDA task under governed gates: run bootstrap checks, route to minimal specialist skills, validate artifacts, and return execution evidence."
---

# EDA Loop

## Role Boundary

`eda-loop` is the execution orchestrator for a scoped task.
Global entry, cross-task governance, and recursion policy belong to `agent.md` (repo root).

Use this skill when you need disciplined execution with explicit artifacts.

## Inputs

Provide or derive:
1. scoped objective,
2. target design/config set,
3. required output artifacts,
4. comparison-policy lock (if claim/comparison is requested).

## Step 1: Bootstrap gates

1. Enter repo root and ensure task brief exists.
2. Run gate before substantive actions:

```bash
bash scripts/common/knowledge_gate.sh --scope <scope_name> --task-brief <task_brief_md>
```

3. Query tool catalog before adding scripts:

```bash
python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>
```

4. Enforce tri-source evidence before non-trivial conclusions:
   - local logs/data,
   - local KB history,
   - internet/primary-source evidence when assumptions are unstable.
5. For infrastructure maintain/develop tasks, run stack guard:

```bash
python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_<tag>
```

## Step 2: Skill routing (minimal set)

Select the smallest set of specialist skills that covers the scoped objective.
Load `references/skill-routing.md` only as needed.

Primary local skills:
- `bspdn-goal-driver`
- `eda-research-chain`
- `eda-knowledge-explorer`
- `eda-idea-debate-lab`
- `eda-hypothesis-experiment-designer`
- `eda-method-implementer`
- `eda-knowledge-gate-maintainer`
- `eda-infra-maintainer`
- `eda-preflight-reflect`
- `eda-retro`
- `eda-stage-checkpoint-golden`
- `gt3-backside-route-policy`
- `delay-model-gate-evaluator`
- `bscost-net`
- `bscost-theory-opt`
- `eda-paper-fetch`
- `eda-pdf-local-summary`

System skills:
- `skill-creator` (create/update skills)
- `skill-installer` (install external skills)

For full-chain research requests, prefer `eda-research-chain` as the primary workflow skill.

## Step 3: Execute under hard gates
1. Announce selected skills and first action.
2. Execute fully (do not stop at plan-only unless asked).
3. For any new experiment submission/comparison request, run `eda-preflight-reflect` first and produce a reflection artifact before launching jobs.
4. For route/CTS submissions, run unified PDK/flow preflight (`scripts/debug/pdk_flow_preflight.py`) and block submission on FAIL.
5. Keep artifact paths explicit (`monitor.md`, `summary.md`, `manifest.tsv`, etc.).
6. After batch completion, run execution-contract validation (`scripts/debug/validate_execution_contract.py`) and mark FAIL rows as non-promotable evidence.
7. Ingest manifest rows into experiment memory (`scripts/common/experiment_memory.py`) and produce constrained follow-up candidates (`scripts/debug/propose_constrained_experiments.py`) when optimization continues.
8. If a gate fails, fix cause before proceeding.
9. Comparison policy lock:
- For algorithmic claims, enforce primary baseline as `vanilla_replace`.
- If Innovus is used, keep it as secondary realizability validation only.
- If only Innovus baseline exists, mark algorithmic conclusion as invalid and stop promotion.

## Step 4: Closeout artifacts

1. Update maintenance log (`slurm_logs/00_meta/knowledge_tool_maintenance_log.md`) for substantive changes.
2. If a skill is modified in this interaction, validate it:

```bash
python3 /home/grads/d/donghao/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill_path>
```

3. Append hypothesis-validation-conclusion entry when a hypothesis was tested:
   - `docs/knowledge_base/90_HYPOTHESIS_VALIDATION_LOG.md`
4. For infrastructure maintain/develop tasks, include both artifacts:
   - `infra_stack_guard` summary
   - `skill_system_audit` summary

## Hard-stop conditions
Do not close task if any condition is true:
1. No maintenance-log update for this interaction.
2. No tool-catalog query evidence for non-trivial changes.
3. Artifacts created but not linked in final summary.
4. Skill modified but not validated.
5. Algorithmic claim made without `vanilla_replace` primary baseline.
6. Route/CTS batch referenced without unified preflight artifact.
7. Route-level conclusion given while execution-contract artifact contains unresolved FAIL rows.

## Out of scope for this skill

1. Defining global entry policy.
2. Defining recursion policy across interactions.
3. Declaring global self-update policy for the whole skill system.
