# Recommended implementation design (phase 1)

2. Add translation linking fields:
3. Project: translation_group_id (UUID, indexed).
4. Lesson: translation_group_id (UUID, indexed).
5. Why: this gives a stable relation between EN/RU twins for future sync/update logic.
6. Add OpenAI integration settings in your dotenv config:
7. OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TIMEOUT_SECONDS.
8. Add fields in Dotenv.py.
9. Build a dedicated service layer:
10. OpenAI client wrapper: retries, timeout, structured JSON response.
11. Content translator service: translate selected text fields while preserving HTML, links, code snippets.
12. Clone service:
    - clone_project_with_translation(source_project, target_lang)
    - clone_lesson_with_translation(source_lesson, translated_project)
13. Hook into admin create flow (most important part):
14. For new Project in admin, after save_related, create translated Project and translated Lessons.
15. For new Lesson in admin, create translated Lesson under the sibling translated Project.
16. Add admin success/warning messages when translation succeeds/fails.
17. On failure: keep original saved, queue retry manually (management command).

## Where to integrate

- Admin orchestration point: admin.py:81
- Add service package under platform_web/services (currently almost empty except model services).
- Env settings source: Dotenv.py:1
- Sync vs async recommendation

## Start sync in admin for MVP:

- Pros: fastest to ship, no infra changes.
- Cons: admin save may be slow (especially project with many lessons).
- Next step (phase 2): DB queue + management command worker (safe on Railway cron/one-off runs).
- Field translation scope

- Project: title, description, stages, seo_title, seo_description.
- Lesson: title, description, objectives, seo_title, seo_description.
- Copy as-is: image/thumbnail, urls, order, type, flags, M2M (framework/programming_languages where meaningful).
- Important edge cases to decide now

## Direction: always RU -> EN, or bidirectional based on source language?

- On creating project with inlines: should translated lessons be generated immediately? (I recommend yes.)
- If translation API fails:
- Create source only and show warning? (recommended)
- Or block save entirely? (not recommended for admin UX)
- Re-translation policy: create-only now, or auto-update translated twin when source is edited?

## Suggested rollout

- Phase 1: Project create auto-clone + lesson clone, synchronous.
- Phase 1.1: Lesson-only create auto-clone to sibling project.
- Phase 2: Retry command + optional async queue.
- Phase 3: Edit synchronization controls.
