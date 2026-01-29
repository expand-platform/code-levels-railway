from django.db import migrations


def seed_website_config(apps, schema_editor):
    WebsiteConfig = apps.get_model("platform_web", "WebsiteConfig")
    WebsiteConfig.objects.get_or_create(
        site_name="CodeLevels", tagline="Your step-by-step coding journey"
    )


def unseed_website_config(apps, schema_editor):
    WebsiteConfig = apps.get_model("platform_web", "WebsiteConfig")
    WebsiteConfig.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("platform_web", "0004_seed_languages"),
    ]

    operations = [
        migrations.RunPython(seed_website_config, unseed_website_config),
    ]
