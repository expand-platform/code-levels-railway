---
name: learn-from-mistakes
description: Log agent mistakes in a project table, read it before similar work, and append new rows after fixes. Use when implementing features, debugging runtime errors, working with Django views/templates/migrations, MODE_SETTINGS filters, or after the agent caused a bug that was corrected.
---

# Learning from Mistakes

Record one-row entries for agent-caused mistakes and their fixes. Read the log before similar work; append after fixing a mistake in the same turn — do not defer.

## Log file

All records live in [`MISTAKES.md`](../development/mistakes/MISTAKES.md).

**Before** starting work in a matching area (views, templates, migrations, static assets, admin, filters, i18n, etc.), read `MISTAKES.md` and scan **Tags** relevant to the task.

**After** you fix a bug that you introduced or could have avoided, append **one row** to the table in `MISTAKES.md` in the same turn as the fix.

## When to log

Log a row when **any** of these is true:

- Runtime error or wrong output caused by your change
- You assumed an API, queryset shape, or template variable without reading the implementation
- You repeated a pattern that already failed in this repo (see existing rows)
- User reported broken behavior after your edit

Do **not** log: user typos, pre-existing bugs you did not touch, or environment/deploy issues outside the code.

## Table format

Keep one markdown table in `MISTAKES.md`. One mistake = one row.

| Date | Area | Mistake | Solution | Tags |
|------|------|---------|----------|------|
| YYYY-MM-DD | module or file | What went wrong (symptom + cause) | What to do instead | comma-separated keywords |

### Column rules

| Column | Write |
|--------|--------|
| **Date** | ISO date when the mistake was found/fixed |
| **Area** | File, module, or subsystem (e.g. `views/projects.py`, `project_filters.html`, `Project` model) |
| **Mistake** | Concrete failure — include error text or user-visible symptom if helpful |
| **Solution** | Actionable rule for next time — one sentence, not a story |
| **Tags** | Short keywords for search (see tag vocabulary below) |

### Tag vocabulary (CodeLevels)

Use these when they apply:

| Tag | Use for |
|-----|---------|
| `views` | FBV/CBV, context dict, MODE_SETTINGS |
| `templates` | Django templates, includes, blocks |
| `models` | Model fields, choices, migrations |
| `migrations` | Schema changes, data migrations |
| `static` | CSS, JS, asset loading |
| `admin` | Jazzmin, `platform_web/admin.py` |
| `i18n` | `{% trans %}`, `_()`, translation blocks |
| `filters` | GET params, search, toggle filters |
| `queryset` | ORM filters, prefetch, ordering |
| `context_processor` | Global sidebar / website_config |
| `urls` | Routing, reverse(), URL names |
| `api` | DRF, `api/` app |

Add new tags when needed; keep them lowercase and short.

## Workflow

```
Task starts
     │
     ▼
Read MISTAKES.md ──match tags?──► Apply listed solutions
     │
     ▼
Implement / fix
     │
     ▼
Agent-caused bug? ──yes──► Append row to MISTAKES.md
     │
     no
     ▼
Done
```

Keep **Solution** to one sentence. Future passes should scan the table in seconds.

## Anti-patterns

- Do not create a separate log file per mistake
- Do not skip logging because the fix was "small"
- Do not write vague rows like "fixed template" — name the variable, filter, or wrong assumption
- Do not log pre-existing issues the user did not ask you to fix

## Related skills

- **Conventions:** `.agents/skills/development/code-style/SKILL.md`
- **Refactor / cleanup:** `.agents/skills/development/refactor/SKILL.md`
- **Environment / venv:** `.agents/skills/development/environment/SKILL.md`
