---
name: codelevels-todo
description: >-
  Product backlog for CodeLevels.net. Use when picking next work, checking
  planned features, or updating the list after completing an item.
---

# Product todo

Remove items when they ship. Add items when the user asks.

Job-first catalog and funnel: [career-tracks](../career-tracks/SKILL.md).

## Job-first (next)

- catalog of job tracks on the public home (teaser for guests, full list after login)
- each track = plan (roadmap) + projects, not a generic language course
- seed / rename `Course` rows to the 12 market job titles
- FAQ per track (and school-wide)
- mentor AI in the founder’s voice
- “Ask the mentor” form on-site → contacts
- changelog page (template/view/model already exist — `changelog.html`, `WebsiteChangelogView`, `Changelog`; still needs URL, entries, and a way to open it)

## Dashboard

Student home (`/dashboard/`). Replace the current recommendation columns with:

- monthly activity
- progress
- current active project
- courses the user is enrolled in

## For my students

- fill in workouts on prod
- update / add new projects for my students (skills related, too)
- each student can now add a profile icon and see where they are on the roadmap

## Course kinds

`Course.type` is the admin dropdown (`job`, `language`, `guide`, `regular`). Regular is the default. Job tracks use job courses; Projects uses regular courses; Roadmaps (`/roadmaps/`) uses language courses. Migration is generated, not applied.

- Guides still have no page (see Extra).

## Extra (additional)

- project details (`/projects/<slug>/`): course progression order is wrong. `project_details_view` loads sibling projects with `.order_by("order", "title")`, while the projects list uses `course_order`. The counter shows the stored `course_order` for projects and the list position for topics, so the number can disagree with the course order
- roadmap page (`/roadmaps/`): Default / List toggle. Default keeps the skill timeline with the outline list items under each skill (`Skill.contents`). List hides those items and shows only the skill names
- drag-and-drop to reorder skills across projects (staff). Projects already reorder inside a skill when workouts are on (`/api/skill/<id>/reorder_projects/`); skills have `order` but the skill groups themselves are not draggable
- GUIDES / Blog posts / articles / tutorials / guides / etc.
- Codelevels Bot + discipline bot + some smart automatizations for student engagement
- when uploading an image, append a unique suffix (random alphanumeric string or uuid4) so filenames don’t collide / cache-bust
