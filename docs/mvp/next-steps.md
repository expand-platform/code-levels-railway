# User Plans

# 1. Models:
- Subscription (general info: name, subscription_level, related user and plan, status, etc)
- PlanUsage (included limits, usage, etc)
- UsageRecord (maybe) (to track usage of each feature, if needed).

# 2. Middleware
- SubscriptionMiddleware to check user subscription status and enforce limits. 
- helpers like get_user_plan(user), allowed_features(user), can_use_feature(user), check_limit(feature) / check_limits(all) 

# 3. Decorators (maybe, like an addition for middleware)
- @subscription_required(feature) to check if user can access a feature before view execution.

# 4. Admin panel
- Manage subscription titles, levels, change levels for users and con  trol usage.

# 5. API endpoints
- View user subscription status, usage, and limits.
- Allow users to upgrade/downgrade subscription levels (if payment integration is added later).
- Allow users to view their usage and limits.
- Allow admin to manage user subscriptions and usage.

# 6. Template tags
- Display subscription status, allowed features, and usage in templates.
- Show upgrade prompts for users nearing limits or on lower tiers.
- Show different content based on subscription level.

# 7. Payment integration (later)
- Integrate with payment providers to handle subscription payments and upgrades.


How It All Connects
1) User hits a view
      ↓
2) @require_feature / @require_limit decorator runs
      ↓
3) Checks Subscription → Plan → feature flags / limits
      ↓
Allowed → view runs normally
Blocked → redirect to /pricing or 403 JSON
      ↓
4) User upgrades → Stripe fires webhook
      ↓
5) Webhook updates Subscription.plan in DB
      ↓
6) Next request immediately sees new plan and features