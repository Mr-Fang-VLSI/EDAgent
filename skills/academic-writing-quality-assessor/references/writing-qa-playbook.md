# Writing QA Playbook

## Scope

Use this workflow for:
- conference and journal papers
- proposals
- dissertations and theses
- long technical reports

## Review Order

1. Build health
- compile with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
- treat build breaks, undefined references, duplicate labels, and missing files as first-priority issues
- treat `Underfull` and `Overfull` boxes as secondary unless they visibly damage layout

2. Structural consistency
- chapter directory names should match chapter roles
- `main.tex` should include only active chapters
- archive old chapters instead of leaving parallel stale versions in the active tree

3. Front matter consistency
- title page, degree name, graduation month, acknowledgements, contributors, and nomenclature must match the current manuscript state
- proposal-specific front matter must not remain in a dissertation

4. Terminology consistency
- standardize first-use expansions and canonical forms
- prefer one canonical form for each term, e.g. `VQ-VAE`, `Bayesian optimization (BO)`, `macro-model`, `I/O`

5. Citation and equation style
- keep one citation style throughout the manuscript
- keep one equation-reference style throughout the manuscript, e.g. `Eq.~\eqref{...}`

6. Figure and table hygiene
- `\includegraphics` paths must match on-disk file names exactly, including case
- prefer short captions and units in table headers
- remove unused figure variants from the cloud project only after local backup

7. Narrative consistency
- each chapter should have a clear opening and a short summary/transition when helpful
- introduction, chapter contributions, and conclusion must describe the same set of contributions

8. Grammar policy
- first pass: fix only mandatory grammar errors
- second pass: improve repetition and transitions
- third pass: refine style only after terminology and structure are stable
