# Agent mistakes log (CodeLevels)

Read before work in matching areas. Append one row per agent-caused mistake when fixed.

Tags: `views`, `templates`, `models`, `migrations`, `static`, `admin`, `i18n`, `filters`, `queryset`, `context_processor`, `urls`, `api`.

| Date | Area | Mistake | Solution | Tags |
|------|------|---------|----------|------|
| 2026-08-05 | project_card.html | Used `{% trans %}` in an included partial without `{% load i18n %}` | Add `{% load i18n %}` at the top of any partial that uses trans/blocktrans | templates, i18n |
| 2026-09-02 | Skill.py | `help_text=_("...")` failed Pylance: lazy proxy is not `str` (Django infers `help_text=""` as `str`) | Wrap model `help_text=_()` with `cast(str, ...)` | models, i18n |
| 2026-09-02 | Roadmap.py | `Model.objects` unknown to basedpyright without django-stubs | Annotate `objects: models.Manager` under `TYPE_CHECKING` on the model | views, models |
| 2026-09-02 | views/Projects.py | Git tracked `projects.py` while the working tree is `Projects.py`; `from .projects` failed locally | Keep PascalCase view modules and `git mv` so Linux/Railway matches the working tree | views |
