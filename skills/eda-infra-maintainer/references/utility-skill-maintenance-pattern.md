# Utility Skill Maintenance Pattern

Use this reference when maintaining or creating utility skills.

## Goal

Keep horizontal capabilities centralized so execution and theory skills only delegate, rather than re-implementing shared logic.

## Required Utility Skill Shape

`SKILL.md` should contain:
1. shared capability boundary,
2. expected downstream consumers,
3. compact input and output contract,
4. explicit escalation path when the utility output implies KB or infra changes,
5. `when to load` mapping for each ref.

## What Must Move Out Of The Entry File

Move to `references/`:
1. step-by-step procedures,
2. command blocks,
3. logging templates,
4. failure handling details,
5. special-case operating notes.

## Split Heuristic

If one utility skill starts owning more than one horizontal concern, split it.

Examples:
1. KB/tool retrieval belongs in `eda-context-accessor`, not in every execution skill.
2. artifact cleanup belongs in `eda-artifact-hygiene-maintainer`, not in infra governance.
3. gate hygiene belongs in `eda-knowledge-gate-maintainer`, not in every loop skill.
