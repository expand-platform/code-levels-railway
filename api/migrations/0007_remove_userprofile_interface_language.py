from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_userprofile_wakatime_api_key"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="interface_language",
        ),
    ]
