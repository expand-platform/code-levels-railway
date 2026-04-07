## Strategy: Project And Lesson Localization (EN/RU)

### Implementation Steps (Quick Execution Order)
1. Install and configure django-parler for Project and Lesson translation models.
2. Add translated fields for Project (title, description, slug, seo_title, seo_description).
3. Add translated fields for Lesson (title, description, slug).
4. Generate and apply migrations for parler translation tables.
5. Backfill English translations from current Project/Lesson source fields.
6. Create Russian translation placeholders and enforce per-language slug uniqueness.
7. Update admin to edit Project/Lesson translations through language tabs only.
8. Refactor project and lesson detail views to resolve localized slugs.
9. Add canonical redirects for stale or wrong-language slugs.
10. Add See in EN / See in RU links to project detail and lesson detail templates.
11. Add fallback behavior for missing sibling translations (hide for users, disabled for staff).
12. Enable i18n URL prefixes (/en and /ru) for website routes.
13. Add canonical and hreflang tags for localized project and lesson pages.
14. Run QA checks for routing, navigation, links, and SEO metadata in both languages.
15. Launch with EN complete first, then publish RU records progressively.

### Goal
Implement bilingual content delivery for projects and lessons with:
- URL prefixes: /en/... and /ru/...
- Localized content fields (title, description, slugs, SEO)
- Language switch links on detail pages: See in EN / See in RU
- Admin-only translation workflow (no external editor/API authoring required)

### Decision: Translation Engine
Use django-parler for Project and Lesson.

Why parler (for your single-source-of-truth requirement):
- One canonical Project/Lesson row with language-specific translation rows.
- Adding a third language later does not require adding new columns.
- Localized slugs and SEO metadata map naturally to per-language translations.

Why not modeltranslation for these models:
- It adds language columns (title_en/title_ru/...) on the base table.
- Each new language typically requires schema updates and wider tables.

Implementation rule:
- Do not run django-parler and django-modeltranslation on the same model.
- Keep existing modeltranslation usage on unrelated models if needed, but use parler for Project/Lesson.

### Success Criteria
1. Project and lesson pages resolve in both languages via prefixed routes.
2. Same entity can be opened in EN and RU from explicit page links.
3. Missing translation has predictable UX (hidden or disabled target-language link).
4. Canonical and hreflang metadata are correct for SEO.
5. Existing navigation and lesson ordering remain stable.

### Recommended Architecture

#### 1) Routing Layer
- Enable language-prefixed routing with Django i18n_patterns only after translated content and localized lookups are in place.
- Keep API and admin routes outside i18n prefixes.
- Preserve language switching endpoint behavior, ensuring redirect respects current prefixed path.

Why:
- Clean SEO-friendly locale URLs.
- Clear separation between UI localization and API/admin endpoints.
- Avoid duplicate content where /en and /ru show identical pages.

#### 2) Translation Data Model
Use django-parler for Project and Lesson.

Fields to translate:
- Project: title, description, slug, seo_title, seo_description
- Lesson: title, description, slug

Guideline:
- Keep stable internal identity via IDs and existing relations.
- Treat localized slugs as presentation URLs, not canonical internal keys.

Why:
- Scales cleanly to 3+ languages without widening core tables.
- Native admin language tabs and per-language editing flow.

#### 3) URL Lookup Strategy
- Resolve project detail by current-language project slug.
- Resolve lesson detail by project + lesson slug in current language (with order fallback only if needed for legacy links).
- Add canonical redirect when request slug mismatches current localized canonical slug.

Why:
- Prevent duplicate pages and SEO dilution.
- Keep old links recoverable while migrating.

#### 4) Cross-Language Linking (Key Requirement)
On both detail pages, compute sibling localized URL for the same entity:
- Project page: See in EN / See in RU
- Lesson page: See in EN / See in RU

Rendering behavior:
- If sibling translation exists: render active link.
- If missing: hide link for users or render disabled state with explanation.

Recommended fallback policy:
- Public users: hide unavailable language link.
- Staff users: show disabled state to expose translation gaps.

#### 5) Admin Authoring Workflow
- Keep translation editing in Django admin only.
- Ensure translated slug + SEO fields are visible per language tab.
- Add short help text indicating that localized slug controls localized URL.

Why:
- Matches your selected workflow.
- Reduces operational complexity.

#### 6) SEO Rules
For project and lesson detail templates:
- Set canonical to current-language canonical URL.
- Emit hreflang links for EN and RU alternates when available.
- Avoid indexing non-canonical stale-slug URLs (redirect first).

Why:
- Prevents duplicate indexing across slug variants.
- Improves search engine language targeting.

### Step-by-Step Rollout

### Phase 1: Translation Schema First
1. Introduce parler translation models for Project and Lesson fields.
2. Include translated slug and SEO fields.
3. Generate and apply migrations.

### Phase 2: Backfill Source Language Data
1. Backfill EN translations from current records.
2. Add RU translation placeholders where needed.
3. Validate slug uniqueness rules in EN and RU.

### Phase 3: Detail Lookup Refactor
1. Update project detail lookup for localized slug.
2. Update lesson detail lookup for localized slug.
3. Add canonical redirect behavior for stale/wrong slugs.

### Phase 4: UI Language Links
1. Add See in EN / See in RU block in project detail template.
2. Add same block in lesson detail template.
3. Add availability-aware rendering logic.

### Phase 5: Enable URL Prefixes
1. Turn on i18n-prefixed web routing (/en and /ru).
2. Validate that each prefixed URL serves localized content.
3. Confirm language switch redirects to the equivalent localized URL.

### Phase 6: SEO And QA
1. Add canonical and hreflang tags.
2. Run URL integrity checks and fix collisions.
3. Verify SEO metadata and alternate-language links.
4. Regression-check listing, detail pages, and lesson navigation.

### Risks And Mitigations
1. Slug collisions in RU
- Mitigation: deterministic slug suffixing and collision audit command.

2. Running both translation frameworks on same model
- Mitigation: enforce framework boundary (parler on Project/Lesson only).

3. Incomplete translations causing broken links
- Mitigation: availability checks before rendering switch links.

4. SEO regressions during slug migration
- Mitigation: canonical redirect map + hreflang validation.

5. Legacy links with old patterns
- Mitigation: temporary compatibility routes and redirect plan.

### Testing Checklist
1. /en/project/... and /ru/project/... both open expected language content.
2. Lesson navigation (prev/next) works in both locales.
3. See in EN / See in RU links point to same entity in other language.
4. Missing sibling translation does not expose broken link.
5. Canonical/hreflang values are correct in page head.
6. Search/filter pages still behave correctly after localization changes.
7. Adding a new language does not require schema changes for Project/Lesson translations.

### Scope Boundaries
Included:
- Project and lesson localization with bilingual routes.
- Localized slugs and SEO metadata.
- Cross-language links on detail pages.
- Admin-only translation editing.

Excluded for now:
- File-based markdown localization pipeline.
- Public translation API/editor tooling.
- Additional locales beyond EN and RU.

### Optional Next Iteration
1. Add bilingual XML sitemap entries for project and lesson variants.
2. Add admin report for missing EN/RU translation coverage.
3. Add redirect history model for changed localized slugs.
