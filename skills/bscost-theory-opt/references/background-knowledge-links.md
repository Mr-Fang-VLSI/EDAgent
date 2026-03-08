# BS Cost Theory Opt Background Knowledge Links

## Core KB Links

Load these when the task is making modeling, promotion, or comparison decisions:
- `docs/knowledge_base/80_BSCOST_THREE_SKILL_WORKFLOW_20260304.md`
- `docs/knowledge_base/84_REPLACE_COMPARISON_POLICY_20260304.md`
- `docs/knowledge_base/82_BACKSIDE_SHORT_NET_DIAGNOSIS_AND_JUDGMENT_MODEL_20260304.md` when short-net judgment or front-vs-back eligibility is relevant
- `docs/knowledge_base/60_NET_COST_MODEL_VS_HPWL_STATUS_20260304.md` when checking whether the current model is still proxy-only or has enough RC/fanout fidelity for promotion

## Paper-derived Background

Use local paper summaries or parsed PDF evidence when:
- choosing physically justified feature blocks,
- deciding whether a cost crossover or capacity term is theoretically plausible,
- checking whether a proposed optimization claim contradicts known backside-routing or delay behavior.

Priority delay-model summaries for the current RC-aware upgrade:
- `docs/papers/summaries/Buffer_placement_in_distributed_RC-tree_networks_for_minimal_Elmore_delay.summary.md`
- `docs/papers/summaries/Modeling_the_Effective_capacitance_for_the_RC_interconnect_of_CMOS_gates.summary.md`
- `docs/papers/summaries/Performance_computation_for_precharacterized_CMOS_gates_with_RC_loads.summary.md`
- `docs/papers/summaries/A_Two_Moment_RC_Delay_Metric_for_Performance_Optimization.summary.md`

These four papers should drive:
- explicit fanout/tree structure terms,
- effective-capacitance or gate-side load compatibility terms,
- higher-order shielding-aware delay features beyond plain Elmore,
- and caution against interpreting total capacitance alone as electrical benefit.

## Integration Rule

If the current task lacks enough local KB or paper-derived context, request scoped retrieval through `eda-context-accessor` before fitting or promotion judgment proceeds.
