# permissions.py
from django.utils import timezone
from .models import Subscription, Plan


def get_user_plan(user) -> Plan:
    """Returns the user's current plan, falling back to free."""
    try:
        sub = user.subscription
        if sub.is_active():
            return sub.plan
    except Subscription.DoesNotExist:
        pass
    return Plan.objects.get(name='free')


def get_entitlements(user) -> dict:
    """Returns a dict of what the user can do."""
    plan = get_user_plan(user)
    return {
        'plan_name': plan.name,
        'max_projects': plan.max_projects,
        'max_ai_credits': plan.max_ai_credits,
        'max_storage_mb': plan.max_storage_mb,
        'max_team_members': plan.max_team_members,
        'can_export': plan.can_export,
        'can_use_api': plan.can_use_api,
        'can_remove_watermark': plan.can_remove_watermark,
        'has_priority_support': plan.has_priority_support,
        'has_advanced_analytics': plan.has_advanced_analytics,
    }


def can_use_feature(user, feature: str) -> bool:
    """Check a single boolean feature flag."""
    entitlements = get_entitlements(user)
    return entitlements.get(feature, False)


def check_limit(user, resource: str) -> tuple[bool, int, int]:
    """
    Check if a user is within their usage limit.
    Returns (allowed, used, limit).
    """
    entitlements = get_entitlements(user)
    usage = getattr(user, 'usage', None)

    limit_key = f'max_{resource}'
    limit = entitlements.get(limit_key, 0)

    used_map = {
        'projects': getattr(usage, 'projects_count', 0),
        'ai_credits': getattr(usage, 'ai_credits_used', 0),
        'storage_mb': getattr(usage, 'storage_used_mb', 0),
    }
    used = used_map.get(resource, 0)

    if limit == -1:  # unlimited
        return True, used, limit

    return used < limit, used, limit