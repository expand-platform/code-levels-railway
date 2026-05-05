from django.db import migrations


def backfill_null_type(apps, schema_editor):
    Lesson = apps.get_model("platform_web", "Lesson")
    Lesson.objects.filter(type__isnull=True).update(type="theory")


class Migration(migrations.Migration):

    dependencies = [
        ("platform_web", "0048_alter_lesson_type"),
    ]

    operations = [
        migrations.RunPython(backfill_null_type, reverse_code=migrations.RunPython.noop),
    ]
