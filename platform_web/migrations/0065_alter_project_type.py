# Generated manually for workout project type

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("platform_web", "0064_alter_blogpost_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="type",
            field=models.CharField(
                choices=[
                    ("topic", "Topic"),
                    ("project", "Project"),
                    ("workout", "Workout"),
                    ("guide", "Guide"),
                ],
                default="topic",
                max_length=20,
            ),
        ),
    ]
