from django.db import migrations

SUFFIX = " | CodeLevels"


def fill_seo_fields(apps, schema_editor):
    Project = apps.get_model("platform_web", "Project")
    Lesson = apps.get_model("platform_web", "Lesson")

    projects = Project.objects.filter(seo_title="")
    
    for project in projects:
        project.seo_title = str(project.title) + SUFFIX
        
    Project.objects.bulk_update(projects, ["seo_title"])

    projects_no_desc = Project.objects.filter(seo_description="")
    
    for project in projects_no_desc:
        project.seo_description = str(project.title)
        
    Project.objects.bulk_update(projects_no_desc, ["seo_description"])

    lessons = Lesson.objects.filter(seo_title="")
    
    for lesson in lessons:
        lesson.seo_title = str(lesson.title) + SUFFIX
    Lesson.objects.bulk_update(lessons, ["seo_title"])

    lessons_no_desc = Lesson.objects.filter(seo_description="")
    for lesson in lessons_no_desc:
        lesson.seo_description = str(lesson.title)
    Lesson.objects.bulk_update(lessons_no_desc, ["seo_description"])


def reverse_fill_seo_fields(apps, schema_editor):
    Project = apps.get_model("platform_web", "Project")
    Lesson = apps.get_model("platform_web", "Lesson")

    projects = Project.objects.filter(seo_title__endswith=SUFFIX)
    for project in projects:
        project.seo_title = ""
    Project.objects.bulk_update(projects, ["seo_title"])

    projects_desc = Project.objects.filter(seo_description__endswith=SUFFIX)
    for project in projects_desc:
        project.seo_description = ""
    Project.objects.bulk_update(projects_desc, ["seo_description"])

    lessons = Lesson.objects.filter(seo_title__endswith=SUFFIX)
    for lesson in lessons:
        lesson.seo_title = ""
    Lesson.objects.bulk_update(lessons, ["seo_title"])

    lessons_desc = Lesson.objects.filter(seo_description__endswith=SUFFIX)
    for lesson in lessons_desc:
        lesson.seo_description = ""
    Lesson.objects.bulk_update(lessons_desc, ["seo_description"])


class Migration(migrations.Migration):

    dependencies = [
        ("platform_web", "0046_alter_project_language"),
    ]

    operations = [
        migrations.RunPython(fill_seo_fields, reverse_code=reverse_fill_seo_fields),
    ]
