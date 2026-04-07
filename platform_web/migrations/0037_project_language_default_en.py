from django.db import migrations, models


def set_project_language_default_en(apps, schema_editor):
    Project = apps.get_model("platform_web", "Project")
    Project.objects.filter(language__isnull=True).update(language="en")
    Project.objects.filter(language="").update(language="en")


class Migration(migrations.Migration):

    dependencies = [
        ("platform_web", "0036_project_language"),
    ]

    operations = [
        migrations.RunPython(
            set_project_language_default_en,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="project",
            name="language",
            field=models.CharField(
                blank=True,
                choices=[("en", "English"), ("ru", "Русский")],
                default="en",
                max_length=50,
                null=True,
            ),
        ),
    ]
