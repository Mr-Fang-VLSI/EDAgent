# Skill Type Patterns

## Goal

Provide stable type boundaries and construction patterns for the skill system so new skills and maintenance work follow a consistent architecture.

## Core Separation Principle

Keep these independent:
1. capability: what the skill does,
2. knowledge: KB docs, paper-derived summaries, and background evidence,
3. tools: reusable scripts, commands, and registry entries.

Skills should connect to knowledge and tools through explicit links, not by duplicating them.

## Skill Types

### 1. Theory-analysis skills

Examples:
- `bscost-theory-opt`
- `eda-theory-veto`

Pattern:
- own theory judgment or model reasoning,
- must include explicit `Background Knowledge Links`,
- must state when paper-derived or KB knowledge must be loaded,
- must explain how contradictions with background knowledge are handled,
- should delegate shared KB/tool retrieval to utility skills.

### 2. Execution skills

Examples:
- `eda-loop`
- `gt3-backside-route-policy`
- `gt3-backside-net-selector`
- `bspdn-goal-driver`

Pattern:
- own scoped execution, gating, and artifact production,
- keep detailed operating procedures in `references/`,
- keep `SKILL.md` focused on scope, inputs/outputs, when to load refs, and when to invoke utility skills,
- should not embed reusable KB/tool retrieval logic directly.

### 3. Utility skills

Examples:
- `eda-context-accessor`
- `eda-infra-maintainer`
- `eda-knowledge-gate-maintainer`
- `git-version-control`
- `eda-artifact-hygiene-maintainer`

Pattern:
- own horizontal capabilities reused by multiple other skills,
- centralize shared logic that would otherwise be duplicated,
- expose compact artifacts or decisions that downstream skills consume,
- must name expected downstream consumers,
- should keep command sequences, logging steps, and failure-policy details in `references/`,
- should not absorb domain conclusions that belong to theory or execution skills.

## Construction Rules By Type

### Theory-analysis skill

`SKILL.md` should include:
- when to use,
- scope boundary,
- background knowledge links,
- when to load each ref,
- when to call utility skills such as `eda-context-accessor`.

### Execution skill

`SKILL.md` should include:
- role boundary,
- inputs and outputs,
- knowledge/tool interaction at delegation level only,
- when to load each operational ref,
- no long step-by-step execution body if that belongs in `references/`.

### Utility skill

`SKILL.md` should include:
- shared capability boundary,
- expected downstream consumers,
- compact output contract,
- escalation path when output implies KB or infra change,
- when to load each operational ref.

## Maintenance Heuristic

If a skill starts mixing:
- reusable horizontal logic,
- domain background knowledge,
- and execution procedure

in one file, split the concerns:
1. move shared logic to a utility skill,
2. move background knowledge to KB or paper-derived artifacts,
3. keep the skill as the capability-layer connector.
