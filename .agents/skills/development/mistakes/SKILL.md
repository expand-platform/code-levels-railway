---
name: codelevels-mistakes
description: >-
  Log agent mistakes in MISTAKES.md and read it before similar work.
  Use when implementing features, debugging runtime errors, working with
  Django views/templates/migrations, MODE_SETTINGS filters, or after a
  bug you caused was corrected.
---

# Learning from Mistakes

Log: [MISTAKES.md](MISTAKES.md)

1. **Before** work in a matching area, read the log and apply rows whose **Tags** match.
2. **After** fixing a bug you introduced or could have avoided, append **one row** in the same turn.

**Log when:** runtime error or wrong output from your change; you assumed an API/queryset/template variable without reading it; you repeated a failed pattern; the user reported a break after your edit.

**Do not log:** user typos, pre-existing bugs you did not touch, env/deploy issues outside the code.

| Date | Area | Mistake | Solution | Tags |
|------|------|---------|----------|------|
| YYYY-MM-DD | file or module | symptom + cause | one-sentence rule | lowercase keywords |

Tags: `views`, `templates`, `models`, `migrations`, `static`, `admin`, `i18n`, `filters`, `queryset`, `context_processor`, `urls`, `api`. Add short lowercase tags as needed.

No extra files per mistake. Do not skip “small” fixes. Name the variable, filter, or wrong assumption — not “fixed template”.
