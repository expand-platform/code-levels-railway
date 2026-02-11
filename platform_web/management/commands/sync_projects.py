# your_app/management/commands/sync_projects.py
from datetime import datetime
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify


from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.Chapter import Chapter
from platform_web.models.app.project.Lesson import Lesson
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Framework import Framework
from platform_web.models.app.project.Skill import Skill
from platform_web.models.app.project.Stage import Stage
from platform_web.models.app.project.Course import Course
from platform_web.models.app.project.Difficulty import Difficulty


class Command(BaseCommand):
    help = "Sync project-related data (Projects, Chapters, Parts) from dev JSON to prod"

    def add_arguments(self, parser):
        parser.add_argument(
            "--media-dir",
            type=str,
            help="Optional: path to media files for images",
            required=False,
        )

    def handle(self, *args, **options):
        backup_dir = os.path.join(settings.BASE_DIR, "backup", "json")
        os.makedirs(backup_dir, exist_ok=True)
        
        filename = f"projects_dump_{datetime.now().strftime('%Y%m%d')}.json"
        file_path = os.path.join(backup_dir, filename)
        
        # collect projects
        projects_data = []
        for proj in Project.objects.all():
            projects_data.append({
                "uuid": str(proj.uuid),
                "title": proj.title,
                "order": proj.order,
                "type": proj.type,
                "course_uuid": str(proj.course.uuid) if proj.course else None,
                "difficulty_uuid": str(proj.difficulty.uuid) if proj.difficulty else None,
                "programming_languages": [{"uuid": str(pl.uuid)} for pl in proj.programming_languages.all()],
                "framework": [{"uuid": str(fw.uuid)} for fw in proj.framework.all()],
                "skills": [{"uuid": str(sk.uuid)} for sk in proj.skills.all()],
                "stages": [{"uuid": str(st.uuid)} for st in proj.stages.all()],
                "is_active": proj.is_active,
                "slug": proj.slug,
                "image": proj.image.name if proj.image else None,
            })

        # collect chapters
        chapters_data = []
        for chap in Chapter.objects.all():
            chapters_data.append({
                "uuid": str(chap.uuid),
                "title": chap.title,
                "order": chap.order,
                "project_uuid": str(chap.project.uuid) if chap.project else None,
                "is_active": chap.is_active,
                "slug": chap.slug,
            })

        # collect parts
        parts_data = []
        for part in Lesson.objects.all():
            parts_data.append({
                "uuid": str(part.uuid),
                "title": part.title,
                "order": part.order,
                "chapter_uuid": str(part.chapter.uuid) if part.chapter else None,
                "is_active": part.is_active,
                "slug": part.slug,
            })

        # combine all
        data = {
            "projects": projects_data,
            "chapters": chapters_data,
            "parts": parts_data,
        }

        # write JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Dump saved to {file_path}"))

        media_dir = options.get("media_dir")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} does not exist"))
            return

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # --- preload FK objects ---
        existing_projects = {p.uuid: p for p in Project.objects.all()}
        chapters = {c.uuid: c for c in Chapter.objects.all()}  # preloaded chapters
        parts = {p.uuid: p for p in Lesson.objects.all()}  # preloaded parts

        courses = {c.uuid: c for c in Course.objects.all()}
        difficulties = {d.uuid: d for d in Difficulty.objects.all()}
        languages = {l.uuid: l for l in ProgrammingLanguage.objects.all()}
        frameworks = {f.uuid: f for f in Framework.objects.all()}
        skills = {s.uuid: s for s in Skill.objects.all()}
        stages = {st.uuid: st for st in Stage.objects.all()}

        # --- sync projects ---
        self.sync_projects(
            dev_projects=data.get("projects", []), # ✅ dev JSON data 
            existing_projects=existing_projects,   # ✅ preloaded DB objects
            courses=courses,
            difficulties=difficulties,
            languages=languages,
            frameworks=frameworks,
            skills=skills,
            stages=stages,
            media_dir=media_dir,
        )

        # --- sync chapters with preloaded projects and chapters ---
        self.sync_chapters(
            dev_chapters=data.get("chapters", []),
            existing_projects=existing_projects,
            chapters=chapters,
        )

        # --- sync parts with preloaded chapters and parts ---
        self.sync_parts(
            dev_parts=data.get("parts", []),
            chapters=chapters,
            parts=parts,
        )

        self.stdout.write(
            self.style.SUCCESS("All projects, chapters, and parts synced successfully!")
        )

    def sync_projects(
        self,
        dev_projects,               # JSON from dev
        existing_projects=None,     # preloaded DB objects if needed
        courses=None,
        difficulties=None,
        languages=None,
        frameworks=None,
        skills=None,
        stages=None,
        media_dir=None,
    ):
        for dev_proj in dev_projects:
            # use preloaded objects instead of querying DB each loop
            course = courses.get(dev_proj.get("course_uuid")) if dev_proj.get("course_uuid") else None
            difficulty = difficulties.get(dev_proj.get("difficulty_uuid")) if dev_proj.get("difficulty_uuid") else None

            # Update or create Project
            project, created = Project.objects.update_or_create(
                uuid=dev_proj["uuid"],
                defaults={
                    "title": dev_proj["title"],
                    "order": dev_proj.get("order", 0),
                    "type": dev_proj.get("type", Project.TOPIC),
                    "course": course,
                    "difficulty": difficulty,
                    "is_active": dev_proj.get("is_active", True),
                    "slug": dev_proj.get("slug") or slugify(dev_proj["title"]),
                },
            )

            # ManyToMany fields
            if "programming_languages" in dev_proj:
                project.programming_languages.set(
                    [
                        languages[pl["uuid"]]
                        for pl in dev_proj["programming_languages"]
                        if pl["uuid"] in languages
                    ]
                )
            if "framework" in dev_proj:
                project.framework.set(
                    [
                        frameworks[fw["uuid"]]
                        for fw in dev_proj["framework"]
                        if fw["uuid"] in frameworks
                    ]
                )
            if "skills" in dev_proj:
                project.skills.set(
                    [
                        skills[sk["uuid"]]
                        for sk in dev_proj["skills"]
                        if sk["uuid"] in skills
                    ]
                )
            if "stages" in dev_proj:
                project.stages.set(
                    [
                        stages[st["uuid"]]
                        for st in dev_proj["stages"]
                        if st["uuid"] in stages
                    ]
                )

            # Handle image (optional)
            if dev_proj.get("image") and media_dir:
                image_path = os.path.join(media_dir, dev_proj["image"])
                if os.path.exists(image_path):
                    with open(image_path, "rb") as img_file:
                        project.image.save(
                            os.path.basename(image_path), img_file, save=True
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Image file {image_path} not found for project {project.title}"
                        )
                    )

            project.save()
            self.stdout.write(
                f"{'Created' if created else 'Updated'} project: {project.title}"
            )

        # Chapters and Parts are now handled in their own methods

    def sync_chapters(self, dev_chapters, existing_projects=None, chapters=None):
        for dev_chap in dev_chapters:
            project = existing_projects.get(dev_chap.get("project_uuid"))
            if not project and dev_chap.get("project_uuid"):
                self.stdout.write(
                    self.style.WARNING(
                        f"Project UUID {dev_chap['project_uuid']} not found for chapter {dev_chap['title']}"
                    )
                )

            chapter, created = Chapter.objects.update_or_create(
                uuid=dev_chap["uuid"],
                defaults={
                    "title": dev_chap["title"],
                    "order": dev_chap.get("order", 0),
                    "project": project,
                    "is_active": dev_chap.get("is_active", True),
                    "slug": dev_chap.get("slug")
                    or f"{slugify(dev_chap['title'])}-{str(dev_chap['uuid'])[:8]}",
                },
            )
            self.stdout.write(
                f"{'Created' if created else 'Updated'} chapter: {chapter.title}"
            )

    def sync_parts(self, dev_parts, chapters=None, parts=None):
        for dev_part in dev_parts:
            chapter = chapters.get(dev_part.get("chapter_uuid"))
            if not chapter and dev_part.get("chapter_uuid"):
                self.stdout.write(
                    self.style.WARNING(
                        f"Chapter UUID {dev_part['chapter_uuid']} not found for part {dev_part['title']}"
                    )
                )

            part, created = Lesson.objects.update_or_create(
                uuid=dev_part["uuid"],
                defaults={
                    "title": dev_part["title"],
                    "order": dev_part.get("order", 0),
                    "chapter": chapter,
                    "is_active": dev_part.get("is_active", True),
                    "slug": dev_part.get("slug")
                    or f"{slugify(dev_part['title'])}-{str(dev_part['uuid'])[:8]}",
                },
            )
            self.stdout.write(
                f"{'Created' if created else 'Updated'} part: {part.title}"
            )
