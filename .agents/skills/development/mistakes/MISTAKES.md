# Agent mistakes log (CodeLevels)

Read this table before work in matching areas. Append one row per agent-caused mistake when fixed.

| Date | Area | Mistake | Solution | Tags |
|------|------|---------|----------|------|
| 2026-08-05 | project_card.html | Used `{% trans %}` in an included partial without `{% load i18n %}` | Add `{% load i18n %}` at the top of any partial that uses trans/blocktrans | templates, i18n |
