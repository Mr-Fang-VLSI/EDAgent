# 115 Academic Writing QA Workflow (2026-03-13)

## Goal

Provide a reusable workflow for academic manuscript writing and quality assurance across:
- dissertations/theses,
- conference and journal papers,
- proposals,
- long technical reports.

## Trigger conditions

Use this workflow when the task is primarily manuscript construction or refinement rather than experimentation.
Examples:
- merge proposal plus papers into a dissertation,
- unify terminology and chapter naming,
- clean LaTeX structure and stale assets,
- run grammar review that only reports must-fix issues.

## Core review order

1. determine the active source closure from `main.tex`
2. confirm front matter matches the current manuscript type
3. audit chapter/section naming against actual manuscript roles
4. unify terminology and style conventions
5. repair graphics-path case mismatches and active asset drift
6. perform grammar review in a must-fix-first order
7. archive stale chapters/assets locally before removing them from the cloud project

## Typical onboarding contexts

Common use cases:
- merge multiple paper drafts into one thesis or dissertation,
- clean a conference/journal manuscript before submission,
- align front matter and chapter roles in a long-form report,
- run a low-risk LaTeX hygiene and terminology audit before deeper rewriting.

## Execution aids

Primary tool:
```bash
python3 scripts/common/latex_writing_audit.py --root <latex_project_root>
```

Primary skill:
- `academic-writing-quality-assessor`

## Expected outputs

- cleaned active chapter tree
- consistent terminology and manuscript structure
- auditable local archive for removed stale material
- concise grammar-fix list when user requests review-only mode
