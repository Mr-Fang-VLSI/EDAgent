# Infrastructure Maintenance Checklist

## Pre-change
1. Confirm mode: `use` / `maintain` / `develop`.
2. Run:
- `python3 scripts/common/infra_stack_guard.py --out-prefix <prefix>`
- `python3 scripts/common/skill_system_audit.py --out-prefix <prefix>`
3. Query existing tools before creating new scripts:
- `python3 scripts/common/tool_catalog.py query <kw1> <kw2>`

## Change
1. Keep edits minimal and scoped to the confirmed gap.
2. Preserve agent/skill boundary in `AGENTS.md`.
3. Update manifest/routing if a new skill is introduced.
4. For any touched skill, enforce reference topology:
- one `references/*.md` file should cover one concrete situation,
- avoid expanding one ref file into a multi-scenario omnibus,
- if `references/*.md` count exceeds `10`, merge same-situation docs or split the skill by responsibility before adding more.
5. For any touched skill, make `SKILL.md` say when to load each referenced file; do not leave the loader decision implicit.
6. For any touched skill, make `SKILL.md` state:
- what KB context must be read or refreshed,
- when `tool_catalog.py query ...` is required,
- what logs/artifacts must be written back to KB or maintenance records.
7. For theory-analysis skills, make `SKILL.md` state:
- which KB docs and paper-derived artifacts provide the professional background basis,
- when that background knowledge must be loaded,
- how contradictions between current proposals and that background knowledge are handled.
8. Classify the touched skill as `theory-analysis`, `execution`, or `utility`, then check it against the corresponding pattern in `references/skill-type-patterns.md`.
9. Preserve separation of capability, knowledge, and tools:
- move reusable background knowledge to KB or paper-derived artifacts,
- move reusable operational logic to utility skills,
- keep skills as bounded connectors rather than monolithic containers.
10. For utility skills, ensure the entry file names:
- expected downstream consumers,
- compact output contract,
- escalation path when the utility result implies KB or infra maintenance,
- and ref-level delegation for commands, logging steps, and failure handling.
11. For architecture changes (routing, workflow ownership, skill boundary, ref-topology policy), record:
- expected benefit hypothesis,
- later validation window,
- falsification signal if the new structure fails to help.

## Post-change
1. Validate changed skills with `quick_validate.py`.
2. Re-run infra guard and skill-system audit.
3. Report:
- changed files,
- artifact paths,
- reference-topology decision for any touched skill,
- architecture-change validation plan when applicable,
- residual risk + rollback trigger.
