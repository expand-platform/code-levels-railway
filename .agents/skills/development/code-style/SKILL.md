---
name: codelevels-code-style
description: >-
  Django code style and project conventions for CodeLevels.net — models, views,
  templates, static assets, admin, and i18n. Use when implementing features,
  adding pages or API endpoints, placing CSS/JS, or when unsure how this repo
  is structured. For cleanup after writing code, use the refactor skill.
---

# CodeLevels Code Style

Educational platform for learning programming through **projects**, **topics**, **workouts**, and **courses**. Stack: Django, Jazzmin admin (`/cp/`), django-allauth, DRF (`api/`), Whitenoise, Railway deploy.

## Principles

1. **Minimize scope** — smallest correct diff; no drive-by refactors while implementing.
2. **OOP / SOLID / DRY** — reuse existing services, mixins, and view patterns before adding new abstractions.
3. **Split modules when justified** — only when a file grows unwieldy or a concern is clearly separable; explain what moved, where, and why.
4. **Match existing conventions** — read surrounding code before writing; new code should look native to the repo.
5. **Cleanup after write** — when the feature works, apply [refactor](../refactor/SKILL.md) on the touched files.

## Project layout

| Path | Role |
|------|------|
| `code_levels/` | Django project settings (`settings/base.py`, `dev.py`, `prod.py`) |
| `platform_web/` | Main web app — models, views, templates, admin, services |
| `api/` | DRF endpoints, Telegram integration, `UserProfile` |
| `static/` | Source CSS/JS (`staticfiles/` is collectstatic output) |
| `content/` | Markdown source for projects/topics (not templates) |

Primary app for UI work: **`platform_web`**.

## Naming conventions

### Models
- Class: PascalCase (`Project`, `Lesson`)
- File: PascalCase in domain folders — `models/project/Project.py`; snake_case in `models/base/`
- Constants: UPPER_SNAKE (`PROJECT`, `WORKOUT`, `PROJECT_TYPE_CHOICES`)
- Explicit `db_table` in plural snake_case (`projects`, `project_parts`)
- SEO/slug: use `SeoSlugMixin` when the model needs public URLs

### Views
- CBV: `{Name}View` (`HomeView`, `SettingsView`)
- FBV: `{resource}_view`, `{resource}_by_{filter}_view` (`projects_view`, `projects_by_course_view`)
- Shared render helpers for list pages — see `MODE_SETTINGS` in `platform_web/views/projects.py`
- Export new views from `platform_web/views/__init__.py`; wire in `platform_web/urls.py`
- Auth: `LoginRequiredMixin` or `@login_required`; paid tiers via `platform_web/decorators.py`

### Templates
- Pages: `platform_web/templates/website/dashboard/pages/{name}.html`
- Partials: `platform_web/templates/website/dashboard/parts/{area}/{name}.html`
- Extend `website/dashboard/parts/layout.html` for dashboard pages
- Use `{% block page_css %}` / `{% block page_js %}` only when layout defaults are insufficient
- Any partial using `{% trans %}` / `{% blocktrans %}` must `{% load i18n %}` at the top

### Static files

CSS is grouped by role:

| Folder | Role |
|--------|------|
| `elements/` | Reusable UI — buttons, cards, badges, toggles, timeline |
| `layout/` | Public shell (`nav.css`, `theme-switch.css`) |
| `layout/dashboard/` | Dashboard shell — sidebar, nav, content chrome, projects sections |
| `pages/` | Page sheets — `home`, `settings`, `lesson_details`, `project_detail`, … |
| `colors/` | Theme tokens (`theme-colors.css`) |

| File | Element |
|------|---------|
| `elements/buttons.css` | Buttons |
| `elements/cards.css` | Project/content cards |
| `elements/badges.css` | Type badges (card meta) |
| `elements/toggles.css` | Toggle switches |
| `elements/timeline.css` | Project timeline |

- Dashboard shell barrel: `layout/dashboard/layout.css` — load from dashboard `layout.html` (do **not** put in public `layout/layout.css`)
- Page CSS: `static/css/pages/{page}.css` — page-specific only; load in `{% block page_css %}`
- JS: `static/js/dashboard/{feature}.js`
- Shared helpers: `static/js/helpers/`, `static/css/colors/theme-colors.css`
- Prefer CSS variables from `theme-colors.css` over hard-coded colors
- Reusable element styles go in `elements/`; register new files in `elements/elements.css`
- Load page-specific assets in template blocks when not global
- Theme tokens must exist in both `data-theme="light"` and `data-theme="dark"` when used

### URLs
- Paths: kebab-case (`desktop-app/`, `projects/course/<slug:course_slug>/`)
- Names: snake_case (`projects_by_course`, `lesson_details`)
- Admin: `/cp/` (not `/admin/`)

## i18n

**English-only UI for now.** Always wrap user-facing strings for future translation:

- Templates: `{% load i18n %}` + `{% trans '...' %}`
- Python models/choices: `gettext_lazy as _`
- Runtime messages in views: `gettext as _`

Do not add Russian `.po` files unless explicitly requested. Content-level language (`Project.language`, translation jobs) is separate from Django i18n.

## Common implementation patterns

### List pages (projects / topics / courses)
`platform_web/views/projects.py` drives three modes via `MODE_SETTINGS`:

```python
MODE_SETTINGS = {
    "projects": {"filter_by": "course", "project_type": "project", ...},
    "topics":   {"filter_by": "language", "project_type": "topic", ...},
    "courses":  {"filter_by": "course", "project_type": "project", "is_video_course": "true"},
}
```

Single template: `website/dashboard/pages/projects.html`. Course blocks use `course.filtered_projects`; attach filtered querysets in the view loop.

### Global template context
`platform_web.context_processors.website_config` provides `website_config`, sidebar nav data (`sidebar_project_courses`, `sidebar_topic_languages`). Use `WebsiteSettings` keys from `platform_web/config/web_config.py` for typed context keys.

### Admin
Register in `platform_web/admin.py`:
- `SortableAdminMixin` for ordered models
- `NestedModelAdmin` + inlines for Project → Lessons
- `SummernoteWidget` for rich text fields
- Fieldsets: General / SEO / Settings

### Services
Business logic in `platform_web/services/model/` (`SlugService`, `SeoService`, …) — static methods, PascalCase `*Service` suffix.

## Feature checklist

When adding a user-facing feature:

1. Model + migration (if new fields/types)
2. View logic + URL (if new page or filter)
3. Template partial or page
4. CSS in the matching dashboard stylesheet; JS if interaction needed
5. Admin fieldsets / filters if staff manage the data
6. `{% trans %}` on all new UI strings
7. Manual check: light + dark theme (`data-theme` on `:root`)
8. Apply [refactor](../refactor/SKILL.md) on touched files

## What to avoid

- New abstractions for one-off logic
- Hard-coded colors instead of theme CSS variables
- Russian UI strings without a translation workflow
- Changing sidebar or unrelated pages when the task is scoped to one list/view
- `localStorage` for server-rendered filters unless persistence across visits is explicitly required — prefer GET params for list filters (same pattern as `search`)
- Leaving unused CSS/theme tokens/comments after a UI change — clean them in the refactor pass

## Related skills

- **Refactor / cleanup:** [refactor](../refactor/SKILL.md)
- **Environment / venv:** [environment](../environment/SKILL.md)
- **Before coding:** [mistakes](../mistakes/SKILL.md) — read [`MISTAKES.md`](../mistakes/MISTAKES.md) for known pitfalls
- **Product scope:** `.agents/skills/product/mvp/SKILL.md`, `.agents/skills/product/todo/SKILL.md`
