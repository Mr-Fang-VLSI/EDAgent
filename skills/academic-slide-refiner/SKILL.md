---
name: academic-slide-refiner
description: Refines and restructures existing presentations into concise, high-impact versions suitable for short academic conference talks (e.g., 20 minutes). Focuses on logical flow, information density, and visual consistency.
license: Complete terms in LICENSE.txt
---

# Academic Slide Refiner

This skill provides a structured workflow for transforming a dense, paper-like presentation into a clear, concise, and compelling talk for a short academic conference slot (e.g., 20 minutes).

## Core Principles

1.  **One Core Idea Per Slide**: Every slide must have a single, clear takeaway. If you have two ideas, make two slides.
2.  **The 5-Second Rule**: An audience member, seeing the slide for the first time, should grasp its main point within 5 seconds without needing to read the whole paper.
3.  **Talk, Don't Read**: Slides are visual aids for the audience, not speaker notes. Use minimal text. The speaker provides the detail.
4.  **Strict Information Diet**: Adhere to these limits:
    *   Maximum 3–4 bullet points per slide.
    *   Maximum 2 lines of text per bullet point.
    *   No long, complex, paper-style sentences.
5.  **Visual Consistency**: A unified style is critical for a professional look. Stick to a simple, high-contrast theme.
    *   **Default Style**: White background, dark text (black or very dark blue), and one or two accent colors for highlighting.
    *   No gradients, shadows, or decorative backgrounds.

## External Report Constraints

For advisor-facing decks:
1. Use English only.
2. Remove internal/local markers from final slides:
   - no absolute paths or local directory names,
   - no long version tags (`*_20260304_192047` style),
   - no internal host/user identifiers.
3. Prefer semantic experiment labels (`Baseline`, `Variant-B`, `Targeted-BM`) over raw run names.
4. If output format is requested as PDF, prioritize `beamer` (`.tex -> .pdf`) and keep a source `.tex` artifact.

## Refinement Workflow

Re-organize the entire presentation to follow a clear, logical narrative. A highly effective structure for technical talks is:

**Problem → Challenges → Key Mechanism → Why It Works → Experimental Validation → Conclusion**

Ensure there are clear transition statements or pages connecting each stage of this narrative.

### Step 1: Restructure and Split

*   **Re-order slides** to fit the causal chain above.
*   **Split complex pages**. A single dense slide should be broken down into multiple simpler slides. For example:
    *   A slide explaining VQ-VAE should be split into: `1. What is VAE?` → `2. What is VQ-VAE (Discrete Latent)?` → `3. Why VQ-VAE Helps Our Problem?`
    *   A slide on Bayesian Optimization should be split into: `1. Why BO is Needed (e.g., Non-differentiable)` → `2. How BO Works in Our Context (e.g., in Latent Space)`.

### Step 2: Content & Layout Refinement

*   **Text**: Ensure font size is large enough for back-of-the-room visibility (>= 22pt is a good rule of thumb).
*   **Layouts**: For common "left text, right image" layouts, ensure content is **vertically centered** to create visual balance. Avoid having a small image next to a large block of text, making the page look lopsided.
*   **Images & Diagrams**:
    *   Images should be large and clear, occupying 40-60% of the slide area.
    *   Ensure diagrams (e.g., model architectures) are stylistically consistent in terms of color, font, and line weight. Use the bundled scripts as a starting point for VAE/VQ-VAE diagrams.
    *   Verify all image paths are correct to prevent broken images showing up as text.
    *   All figures must have clear, numbered captions (e.g., "Fig. 1(a): ...").

### Step 3: Enforce Academic Rigor

*   **Define Acronyms**: Spell out all acronyms on their first appearance. For example: `MMM (Machine Learning-Based Macro-Modeling)`.
*   **Add References**: For all prior work mentioned (e.g., ALIGN, MMM), add a citation number `[X]` in the text. At the bottom of the slide, add a corresponding reference footnote.
*   **Re-number References**: The reference numbering should follow the order of appearance **in the slides**, not the order from the original paper.

## Page-Specific Best Practices

*   **Motivation Pages**: Clearly show the problem. Use contrasting visuals (e.g., Schematic vs. Layout performance) to highlight the performance gap. Explicitly state why existing solutions (e.g., HPWL) are insufficient.
*   **"Why X in Y?" Pages**: The focus should be on the synergy. The question is not "Why use Bayesian Optimization?" but "Why is Bayesian Optimization effective *in Latent Space*?". The key is to explain the advantages gained from the combination (e.g., Feasibility Guarantee, Dimensionality Reduction).
*   **Limitations Pages**: When discussing the limitations of prior work (e.g., MMM), be direct and use simple language. A text-only, centered layout with large fonts can be very effective for impact.

## Bundled Resources

*   `scripts/gen_vae_diagram.py`: A Python script using Matplotlib to generate a VAE architecture diagram with a clean, academic style.
*   `scripts/gen_vqvae_diagram.py`: A Python script to generate a VQ-VAE architecture diagram, stylistically matching the VAE diagram.
