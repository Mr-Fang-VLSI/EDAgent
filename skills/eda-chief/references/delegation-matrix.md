# Delegation Matrix

Top-level routing policy lives in repo `agent.md`; this matrix is compatibility guidance for legacy `eda-chief` calls.

Use minimal-set delegation:

1. Entry and governed execution
- `eda-loop`
 - `eda-theory-veto` (pre-submit theory sanity gate)

2. Pre-run diagnosis
- `eda-preflight-reflect`

3. Post-run retrospective and recursion decision
- `eda-retro`

4. Cost-model and benchmarking
- `bscost-net`
- `bscost-theory-opt`
- `delay-model-gate-evaluator`
- `eda-paper-fetch`
- `eda-pdf-local-summary`

5. Flow/PDK/backside routing policy
- `gt3-backside-route-policy`

6. Checkpoint/golden management
- `eda-stage-checkpoint-golden`

7. Skill creation/update/install
- `skill-creator`
- `skill-installer`

8. Execution foundation utilities (called inside `eda-loop`)
- `scripts/debug/pdk_flow_preflight.py`
- `scripts/debug/validate_execution_contract.py`
- `scripts/common/experiment_memory.py`
- `scripts/debug/propose_constrained_experiments.py`
- `scripts/debug/run_autonomy_foundation_cycle.sh`

9. Presentation/reporting
- `academic-presentation-crafter`
- `academic-slide-refiner`

10. Infrastructure maintenance/development
- `eda-infra-maintainer`
- `scripts/common/infra_stack_guard.py`
- `scripts/common/skill_system_audit.py`

11. End-to-end research chain
- `eda-research-chain`
- `eda-knowledge-explorer`
- `eda-idea-debate-lab`
- `eda-hypothesis-experiment-designer`
- `eda-method-implementer`
- `scripts/common/init_research_chain.py`
- `scripts/common/research_chain_guard.py`

12. Explicit BSPDN target driving
- `bspdn-goal-driver`
- `scripts/debug/track_bspdn_goal_progress.py`
- `scripts/debug/generate_bspdn_goal_campaign.py`

Selection rules:
1. prefer one primary + one diagnostic + one validation skill.
2. avoid running multiple similar optimization skills in the same loop unless comparing explicit hypotheses.
3. for high-cost/high-risk proposals, run `eda-theory-veto` before submission.
4. if request includes formula/model/gradient/differentiability, `bscost-theory-opt` is mandatory and runs before `eda-loop`.
5. every execution update must include explicit `Skills used:` declaration.
