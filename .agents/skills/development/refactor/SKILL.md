---
name: codelevels-refactor
description: >-
  Clean up CodeLevels code after implementation — dead code, duplication,
  readability, performance. Use after writing or changing features, or when
  the user asks to refactor, clean up, or remove unused styles/comments.
---

# CodeLevels Refactor

Run after a feature/fix (same session) unless the user skips cleanup. Stay on **files touched in this task**.

After the pass, **report to the user** (do not only edit silently):

| | |
|--|--|
| **Where** | File / symbol / partial |
| **Why** | Dead, duplicated, or unclear |
| **What improved** | Readability, DRY, performance, fewer bugs |

Skip whitespace-only noise. If nothing to change, say so in one sentence.

## Checklist

**Dead** — unused imports/vars/functions/classes/`{% load %}`; CSS selectors and `theme-colors.css` tokens with no consumers; commented-out stubs; empty markup branches.

**Dupe** — same styles in page CSS and `elements/` / `layout/` (keep one home); repeated template conditionals that belong in a partial/filter.

**Maintain** — match [code-style](../code-style/SKILL.md) naming/placement; CSS variables over hard-coded colors; GET params for list filters.

**Perf** — N+1 / missing `select_related`/`prefetch_related` on list pages you touched; do not load unused page CSS/JS; fix bottlenecks only in scoped files.

## Out of scope

New features disguised as cleanup. Whole-repo reformat. Deleting “unused” public API / admin / migrations without confirming.
