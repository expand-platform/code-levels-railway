from django.db import migrations


def seed_stages(apps, schema_editor):
    Stage = apps.get_model("platform_web", "Stage")
    stages = [
        ("HTML/CSS: UI, UX", 1),
        ("JavaScript: client, interactivity", 2),
        ("Backend: server, database", 3),
        ("Refactoring", 4),
        ("Deployment", 5),
        ("Tests", 6),
    ]
    for name, order in stages:
        Stage.objects.get_or_create(name=name, defaults={"order": order})


def unseed_stages(apps, schema_editor):
    Stage = apps.get_model("platform_web", "Stage")
    Stage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("platform_web", "0005_seed_website_configuration"),
    ]

    operations = [
        migrations.RunPython(seed_stages, unseed_stages),
    ]
