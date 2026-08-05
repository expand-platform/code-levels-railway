---
name: codelevels-refactor
description: >-
  Clean up CodeLevels code after implementation — remove dead code, dedupe,
  tighten maintainability and performance. Use after writing or changing
  features, when the user asks to refactor, clean up, remove unused styles
  or comments, or review recently edited files for waste.
---

# CodeLevels Refactor

After the code is written, analyze it and make sure it is clean and efficient:

- unused comments / imports / variables / functions / classes are removed
- duplicate code is removed
- code is formatted to improve readability
- code is optimized to improve performance
- code is improved to be more maintainable
- if there some kind of bottleneck, you need to identify it and improve it

## When to run

1. **After** a feature or fix is implemented (same session), unless the user says to skip cleanup.
2. When the user explicitly asks to refactor, clean up, or remove unused styles/comments.
3. Prefer the **files touched in this task** — do not expand into unrelated drive-by refactors unless asked.

## Workflow

```
Implementation done
       │
       ▼
Read code-style skill for conventions
       │
       ▼
Scan touched files (and their direct dependents)
       │
       ▼
Remove / dedupe / tighten (checklist below)
       │
       ▼
Re-check: templates ↔ CSS/JS ↔ theme tokens still match
       │
       ▼
Report to the user (required — see below)
       │
       ▼
Done (log to mistakes skill only if you introduced a bug)
```

## Report after every refactor (required)

After finishing a refactor pass, **always write the user a short report** of what changed. Do not only silently edit files.

For each meaningful change, explain:

| | |
|--|--|
| **Where** | File / symbol / template partial |
| **Why** | What was wrong, duplicated, dead, or unclear |
| **What improved** | Readability, DRY, performance, fewer bugs, easier change later |

Keep the report pointed: group by area if many files; skip trivial whitespace-only noise. If nothing worth refactoring was found, say so in one sentence.

## Checklist (CodeLevels)

### Dead code
- Unused imports, variables, functions, classes, template tags/`{% load %}`
- CSS selectors and theme tokens (`theme-colors.css`) with no template/JS consumers
- Commented-out code and leftover “kept for later” stubs that are not wired
- Empty markup branches that never render content

### Duplication
- Same styles or logic in page CSS and `elements/` / `layout/` files — keep one home
- Repeated template conditionals that belong in a partial or filter

### Readability & maintainability
- Match naming and file placement from [code-style](../code-style/SKILL.md)
- Prefer CSS variables over hard-coded colors when touching styles
- Prefer GET params for list filters (same pattern as `search`)

### Performance
- Spot N+1 / missing `select_related`/`prefetch_related` on list pages you touched
- Avoid loading unused page CSS/JS; keep page CSS as imports + page-specific layout only
- Flag real bottlenecks; fix only within the scoped files unless the user widens scope

## Out of scope

- New features or behavior changes disguised as cleanup
- Reformatting the whole repo
- Deleting “unused” public API / admin / migrations without confirming

## Related skills

- **Conventions:** [code-style](../code-style/SKILL.md)
- **Environment / venv:** [environment](../environment/SKILL.md)
- **Mistakes log:** [mistakes](../mistakes/SKILL.md)
