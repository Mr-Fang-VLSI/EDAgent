---
name: academic-presentation-crafter
description: Creates and refines high-quality academic presentations from research papers. Use this skill for tasks involving the conversion of scientific or technical documents into slide decks for conferences, lectures, or academic reviews.
---

# Academic Presentation Crafter

## Overview

This skill provides a structured, multi-phase workflow for transforming dense research papers into clear, concise, and academically rigorous presentations. It ensures the final slide deck is not only visually polished but also accurately reflects the paper's core contributions, data, and terminology.

## Workflow

The process is divided into four distinct phases. Follow these steps sequentially to ensure a high-quality outcome. For detailed checklists on rigor and visual polish, refer to the `references/` directory.

## External Advisor Mode (Required for committee/group reports)

When the audience is external (advisor, committee, collaborator), enforce:
1. English-only slide text.
2. No local machine/repo disclosure:
   - remove absolute paths,
   - remove local usernames/hostnames,
   - replace run IDs/version-like suffixes with semantic labels (e.g., `Baseline`, `Variant-B`).
3. Prefer neutral artifact naming in slides (`Case-A`, `Case-B`) and move raw identifiers to private appendix only if requested.
4. If slide tooling allows, produce `beamer` (`.tex`) and compile to `.pdf`; otherwise keep a clean Markdown deck as fallback.

Action: follow `references/external_reporting_sanitization_checklist.md` before finalizing.

### Phase 1: Foundational Analysis & Outline Generation

The goal of this phase is to deeply understand the source material and create a logical structure for the presentation.

1.  **Initial Skim & Core Contribution Identification**: Read the paper's abstract, introduction, and conclusion to grasp the main argument, key contributions, and overall narrative.
2.  **Identify Key Figures & Data**: Scan the paper for essential figures, charts, tables, and equations that are critical for explaining the methodology and results. Note their figure numbers and captions.
3.  **Generate a Comprehensive Outline**: Create a slide outline. If slide tooling is unavailable, generate a Markdown deck (`.md`) with `---` page separators. A typical academic structure is recommended (Motivation, Methods, Results, Conclusion). Start with 8-12 slides and expand only if necessary.

### Phase 2: Content Drafting & Asset Integration

This phase focuses on populating the slides with content and integrating the necessary visual aids.

1.  **Draft Slide Content**: Write the content for each slide. Paraphrase the paper's content into concise bullet points and short sentences.
2.  **Integrate Visuals**: Incorporate the key figures and diagrams identified in Phase 1. Ensure images are high-resolution and placed logically.
3.  **Data Placeholders**: For slides that will contain charts or graphs, clearly note the data source from the paper. Do not invent or approximate data.

### Phase 3: Academic Rigor & Content Refinement

This is the most critical phase for ensuring the presentation meets academic standards. It requires meticulous attention to detail.

**Action**: Read and meticulously follow the checklist in `references/academic_rigor_checklist.md`.

This checklist covers:
-   Data and Metrics Verification
-   Terminology and Acronyms
-   Claims and Contributions
-   Explanations and Notations

### Phase 4: Visual Polish & Final Review

This final phase focuses on aesthetics, readability, and overall presentation quality.

**Action**: Read and meticulously follow the checklist in `references/visual_polish_checklist.md`.

This checklist covers:
-   Readability and Typography (e.g., min 18pt font size)
-   Layout and Consistency
-   Visual Cohesion
-   Final Review Steps

## Key Principles

-   **Academic Integrity First**: The presentation must be a faithful representation of the research paper.
-   **Clarity and Conciseness**: Slides should support the speaker, not replace them.
-   **Consistency is Professional**: A consistent visual style signals a well-prepared presentation.
