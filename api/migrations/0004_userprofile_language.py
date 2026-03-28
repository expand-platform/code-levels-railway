from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_userprofile_telegram_first_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="interface_language",
            field=models.CharField(max_length=10, blank=True, default=""),
        ),
    ]
