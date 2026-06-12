from django.db import migrations


def assign_free_plan(apps, schema_editor):
    PaidPlan = apps.get_model("platform_web", "PaidPlan")
    UserProfile = apps.get_model("api", "UserProfile")

    free_plan, _ = PaidPlan.objects.get_or_create(
        title="Free",
        defaults={
            "access_level": 0,
            "ui_order": 0,
            "name": "Free",
        },
    )

    UserProfile.objects.filter(paid_plan__isnull=True).update(paid_plan=free_plan)


def revert_free_plan_assignment(apps, schema_editor):
    PaidPlan = apps.get_model("platform_web", "PaidPlan")
    UserProfile = apps.get_model("api", "UserProfile")

    try:
        free_plan = PaidPlan.objects.get(title="Free", access_level=0)
    except PaidPlan.DoesNotExist:
        return

    UserProfile.objects.filter(paid_plan=free_plan).update(paid_plan=None)


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_userprofile_paid_plan"),
        ("platform_web", "0056_seed_paid_plans"),
    ]

    operations = [
        migrations.RunPython(assign_free_plan, revert_free_plan_assignment),
    ]
