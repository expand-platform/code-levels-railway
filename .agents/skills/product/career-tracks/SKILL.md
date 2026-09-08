---
name: codelevels-career-tracks
description: >-
  Job-first catalog and sales funnel for CodeLevels.net. Use when adding
  tracks, courses, roadmaps, homepage, FAQ, mentor AI, contacts, or gating
  content behind login.
---

# Career tracks (job-first)

CodeLevels is a **job-search-first** school: a visitor picks a market job title,
then dives into that track (plan, projects, FAQ, mentor). Do not invent
generic “learn Python” courses as the top-level product. Tracks are real
vacancies from job boards.

English UI strings. `Course` maps to one **track** (job title), not a
language. Group tracks by **family** in the catalog UI only.

## Families and tracks

Titles and slugs for the future `Course` seed (`is_job_course=True`). Do not invent extra tracks.

### Python

| Track | Slug |
|-------|------|
| Python AI Engineer | `python-ai-engineer` |
| Python Web Scraping / Antibot Engineer | `python-web-scraping-antibot-engineer` |
| Python Web Scraping / Data Collection Engineer | `python-web-scraping-data-collection-engineer` |
| Python Automation Engineer | `python-automation-engineer` |
| Python ERP / Odoo Developer | `python-erp-odoo-developer` |
| Python Django / Full-Stack Developer (React) | `python-django-fullstack-developer` |

### Frontend

| Track | Slug |
|-------|------|
| Frontend VueJS Developer | `frontend-vuejs-developer` |
| Frontend ReactJS Developer | `frontend-reactjs-developer` |

### QA

| Track | Slug |
|-------|------|
| QA Engineer / Security Specialist | `qa-engineer-security-specialist` |

### Security

| Track | Slug |
|-------|------|
| Cyber Security Analyst / SOC Analyst | `cyber-security-analyst-soc-analyst` |

### Data

| Track | Slug |
|-------|------|
| Python ML / Data Science Engineer | `python-ml-data-science-engineer` |

### DevOps

| Track | Slug |
|-------|------|
| DevOps Engineer | `devops-engineer` |

Do not add a track unless it matches a vacancy title on job boards.
Keep title spelling as in the table (**VueJS**, **ReactJS**, **Antibot**, **Odoo**).

## Sales funnel (on-site)

Every public surface is a step toward login → FAQ/AI → mentor contact.

1. **Catalog** — families + tracks. Nav label is **Roadmap** (`/roadmap/`).
   **Projects** (`/projects/`) is course → projects + workouts; `?view=roadmap`
   is course → skill → projects. The previous flat URL `/old/` aliases the same
   page. Guests see a teaser list; full catalog after login (“Sign in to see the
   full list”).
2. **Track** — plan (roadmap skills) + projects for that job title.
3. **FAQ** — common questions for the track / school.
4. **Mentor AI** — answers in the founder’s voice (same person as the
   mentor), not a generic chatbot.
5. **Ask the mentor** — form on the site, wired to contacts.

Do not hide the catalog entirely from guests. Tease, then gate depth.

## Existing models

Reuse `Course` → `Skill` → `Project`. Homepage and sidebar should lead with
tracks, not a flat project dump. Landing / “Learn with mentor” stays the
paid/mentor CTA at the end of the funnel, not the first screen.
