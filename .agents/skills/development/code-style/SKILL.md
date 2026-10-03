---
name: codelevels-code-style
description: >-
  Django conventions for CodeLevels.net — models, views, templates, static
  assets, admin, and i18n. Use when implementing features, adding pages or
  API endpoints, placing CSS/JS, or when unsure how this repo is structured.
  After writing code, apply the refactor skill. Before similar work, scan
  the mistakes log.
---

# CodeLevels Code Style

Educational platform: **projects**, **topics**, **workouts**, **courses**, **roadmap**.
Stack: Django, Jazzmin (`/cp/`), django-allauth, DRF (`api/`), Whitenoise, Railway.

**Before coding:** scan [MISTAKES.md](../mistakes/MISTAKES.md) for matching tags.
**After coding:** apply [refactor](../refactor/SKILL.md) on touched files.
Python commands: `poetry run` — see [environment](../environment/SKILL.md).

## Principles

1. Smallest correct diff — no drive-by refactors while implementing.
2. Reuse existing services, mixins, and view patterns (OOP / SOLID / DRY).
3. Split a module only when it is unwieldy; say what moved and why.
4. Read surrounding code first; match local conventions.

## Layout

| Path | Role |
|------|------|
| `code_levels/` | Settings (`base.py`, `dev.py`, `prod.py`) |
| `platform_web/` | Main app — models, views, templates, admin, services |
| `api/` | DRF, Telegram, `UserProfile` |
| `static/` | Source CSS/JS (`staticfiles/` = collectstatic) |
| `content/` | Markdown for projects/topics (not templates) |

UI work lives in **`platform_web`**.

## Naming

**Models** — PascalCase class (`Project`); PascalCase file in domain folders (`models/project/Project.py`), snake_case in `models/base/`; `UPPER_SNAKE` constants; explicit plural-snake `db_table`; `SeoSlugMixin` for public URLs.

**Views** — CBV `{Name}View`; FBV `{resource}_view` / `{resource}_by_{filter}_view`. List pages share `MODE_SETTINGS` in `platform_web/views/Projects.py`. Export from `platform_web/views/__init__.py`; wire in `platform_web/urls.py`. Auth: `LoginRequiredMixin` / `@login_required`; paid tiers: `platform_web/decorators.py`.

Import the **git-tracked** module name. View files are PascalCase (`Roadmap.py`, `Projects.py`, `Home.py`). Windows can hide a lowercase git path; `git mv` so Railway/Linux matches the working tree.

**Templates** — pages `.../dashboard/pages/{name}.html`; partials `.../parts/{area}/{name}.html`; extend `website/dashboard/parts/layout.html`. Use `{% block page_css %}` / `{% block page_js %}` only when layout defaults are insufficient. Any partial with `{% trans %}` / `{% blocktrans %}` must `{% load i18n %}` at the top.

**URLs** — paths kebab-case; names snake_case; admin is `/cp/` (not `/admin/`).

## Static files

| Folder | Role |
|--------|------|
| `elements/` | Reusable UI (buttons, cards, badges, toggles, timeline) |
| `layout/` | Public shell |
| `layout/dashboard/` | Dashboard shell (sidebar, nav, chrome) |
| `pages/` | Page-specific sheets |
| `colors/` | Theme tokens (`theme-colors.css`) |

- Dashboard barrel: `layout/dashboard/layout.css` — load from dashboard `layout.html`, **not** public `layout/layout.css`
- Page CSS: `static/css/pages/{page}.css` in `{% block page_css %}`
- JS: `static/js/dashboard/{feature}.js`; shared helpers: `static/js/helpers/`
- Register new element files in `elements/elements.css`
- Colors: variables from `theme-colors.css`; define tokens in both `data-theme="light"` and `data-theme="dark"`
- Detail-page back links: `data-smart-back` + `static/js/helpers/smartBack.js` (list URL in `sessionStorage`, not `localStorage`)

## i18n

English-only UI for now, but wrap every user-facing string:

- Templates: `{% load i18n %}` + `{% trans '...' %}`
- Models/choices: `gettext_lazy as _`
- View messages: `gettext as _`

No Russian `.po` files unless asked. `Project.language` / translation jobs are separate from Django i18n.

## Patterns

**List pages** (`projects` / `topics` / `courses`) — one view, `MODE_SETTINGS`:

```python
MODE_SETTINGS = {
    "projects": {"filter_by": "course", "project_type": "project", ...},
    "topics":   {"filter_by": "language", "project_type": "topic", ...},
    "courses":  {"filter_by": "course", "project_type": "project", "is_video_course": "true"},
}
```

Template: `website/dashboard/pages/projects.html`. Course blocks use `course.filtered_projects` (attach in the view loop).

**Roadmap** — `JobsView` at `/roadmap/` (job tracks). **Projects** — `projects_page_view` at `/projects/` (course → projects; non-job). `?view=roadmap` is `RoadmapView` (course → skill → projects). **Languages** — `LanguagesView` at `/languages/` (language courses → skills, including skills with no projects). Skills belong to a course; projects M2M ordered by `Project.skill_order`. Sidebar and `/roadmap/` list job courses that have at least one skill, including skills with no projects. Courses with no skills are left out of the sidebar and the roadmap. Language courses with no skills still appear on `/languages/`. Context: `sidebar_job_courses`, `sidebar_project_courses`, `sidebar_language_courses`. Staff reorder when workouts are on: `/api/skill/<id>/reorder_projects/`.

**Context** — `platform_web.context_processors.website_config` → `website_config`, `sidebar_project_courses`, `sidebar_job_courses`, `sidebar_topic_languages`. Typed keys: `platform_web/config/web_config.py`.

**Admin** (`platform_web/admin.py`) — `SortableAdminMixin`; `NestedModelAdmin` + inlines for Project → Lessons; `SummernoteWidget` for rich text; fieldsets General / SEO / Settings.

**Services** — `platform_web/services/model/` (`SlugService`, `SeoService`, …), static methods, `*Service` suffix.

## Feature checklist

1. Model + generate migration (`makemigrations`); check it, do not apply — see [environment](../environment/SKILL.md)
2. View + URL
3. Template (page or partial)
4. CSS in the matching sheet; JS if needed
5. Admin fieldsets/filters if staff-managed
6. `{% trans %}` on new UI strings
7. Check light + dark (`data-theme` on `:root`)
8. Refactor pass on touched files

## Avoid

- New abstractions for one-off logic
- Hard-coded colors; unused CSS/theme tokens/comments after a UI change
- Russian UI strings without a translation workflow
- Changing sidebar/unrelated pages when the task is one list/view
- `localStorage` for server-rendered list filters — use GET params (same as `search`)
