# Skill Reference Topology Policy

## Goal

Keep each skill's `references/` directory easy to route and cheap to read.

## Rules

1. One reference document should handle one concrete situation only.
2. Do not accumulate multiple unrelated scenarios into a single long reference document just because they belong to the same skill.
3. If a reference document starts mixing checklist, exception table, examples, and recovery flow for different situations, split it into multiple files and keep the skill entrypoint responsible for routing.
4. If a skill has more than 10 markdown files under `references/`, refactor before adding more:
- merge files that are truly the same situation with duplicated setup or duplicated decision logic,
- or split the skill into narrower skills if the file count reflects multiple responsibilities rather than one responsibility with normal depth.
5. Prefer adding a new reference file over extending an existing one when the new content changes the triggering condition or output contract.
6. `SKILL.md` must explicitly state when each reference file should be loaded; a bare unordered list of ref files is insufficient.
7. `SKILL.md` must describe the skill's interaction logic with the knowledge base and tool registry, including when KB context is required, when tool reuse must be checked, and what artifacts/logs must be written back.
8. Theory-analysis skills must explicitly link themselves to professional background knowledge in the knowledge base and paper-derived evidence; specialist professionalism is not valid if the skill is detached from the domain knowledge it depends on.

## Merge vs Split Decision

Use merge when:
- two reference files share the same trigger condition,
- they produce the same artifact shape,
- the distinction is only a small variant or parameter choice.

Use skill split when:
- the reference set exceeds 10 because the skill is handling multiple responsibilities,
- different references imply different tools, artifacts, or validation gates,
- the skill entry logic is becoming a workflow router instead of a specialist.

## Review Heuristics

Treat a reference document as high-risk and review for splitting when:
- it is clearly read only in fragments for different situations,
- new sections are being added as exceptions instead of a clean flow,
- it becomes difficult to name the file after a single situation,
- the document grows past roughly 200 lines without being a pure table/template/checklist.

## Required Maintenance Action

When touching a skill:
1. Check whether the new situation can live in an existing single-situation file without broadening its scope.
2. Check the total `references/*.md` count for that skill.
3. If count > 10, include an explicit merge-or-split decision in the change report.
4. Ensure `SKILL.md` contains a `when to load` mapping for every listed reference file.
5. Ensure `SKILL.md` contains explicit knowledge-base and tool-registry interaction logic.
6. For theory-analysis skills, ensure `SKILL.md` explicitly links to the KB and paper-derived background knowledge that the skill relies on.
