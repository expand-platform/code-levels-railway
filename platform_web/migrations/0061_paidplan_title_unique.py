from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("platform_web", "0060_seed_paidplan_prices"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="paidplan",
            constraint=models.UniqueConstraint(fields=["title"], name="paidplan_title_unique"),
        ),
    ]
