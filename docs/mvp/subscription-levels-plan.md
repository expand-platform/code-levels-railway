# Subscription/Supporter Level Plan

## Goal
Add admin-managed subscription levels for website users, enabling future feature gating and visibility based on support tier.

## Approach
1. Create a new `SupporterLevel` model in `api/models`.
   - Fields:
     - `level` (PositiveSmallIntegerField, unique)
     - `name` (CharField)
     - `description` (TextField, optional)
     - `is_active` (BooleanField, default True)
   - Order by `level` and use `__str__` for easy admin display.

2. Add `supporter_level` to `UserProfile`.
   - ForeignKey to `SupporterLevel`.
   - Allow `null`/`blank` for existing users and default to a free tier if none assigned.
   - Add helper methods for comparability and feature checks.

3. Register models in `api/admin.py`.
   - Show `supporter_level` in `UserProfileAdmin`.
   - Add `SupporterLevel` admin listing.

4. Create migrations.
   - schema migration for new model and profile field.
   - optional data migration to seed default tiers: `free=0`, `premium=1`, `top 1% start=2`, others=3.

5. Expose the current tier in profile/settings UI.
   - Update relevant settings views and templates if required.

6. Add tests.
   - Verify default level assignment.
   - Verify support tier comparability.
   - Verify admin-managed level assignment.

## Verification
- Run `python manage.py makemigrations api`.
- Run `python manage.py migrate`.
- Confirm admin can manage `SupporterLevel` and assign it to profiles.
- Confirm helper methods work in shell.
- Add tests in `api/tests.py`.

## Notes
- This is an initial implementation focused on admin-managed tiers and integer comparability.
- Actual payment flow and gated feature visibility can be added in later iterations.
