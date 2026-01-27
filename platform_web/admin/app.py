from django.contrib import admin
from django_summernote.widgets import SummernoteWidget
from django import forms

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from platform_web.models.app.project.Course import Course
from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.Part import Part
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Difficulty import Difficulty
from platform_web.models.app.project.Stage import Stage
from platform_web.models.app.project.Skill import Skill
from platform_web.models.app.project.Review import Review
from platform_web.models.app.project.Submission import Submission
from platform_web.models.app.project.Framework import Framework
from platform_web.models.app.project.Chapter import Chapter
from platform_web.models.app.project.ChapterPart import ChapterPart


class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("title", "order")
    search_fields = ("title",)


class SkillsAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class StagesAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class FrameworkAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class ChapterPartInline(SortableInlineAdminMixin, NestedTabularInline):
    model = ChapterPart
    extra = 1
    fields = ("part", "custom_title", "order")
    autocomplete_fields = ["part"]
    ordering = ["order"]


class ChapterInline(SortableInlineAdminMixin, NestedTabularInline):
    model = Chapter
    extra = 1
    fields = ("title", "order", "description")
    ordering = ["order"]


class ProjectAdmin(SortableAdminMixin, NestedModelAdmin):  # type: ignore[misc]
    inlines = [ChapterInline]
    list_display = (
        "title",
        "course",
        "type",
        "difficulty",
        "get_programming_languages",
        "get_framework",
        "chapter_count",
        "updated_at",
        "is_active",
        "order",
    )
    list_filter = ("difficulty", "programming_languages",  "framework", "type", "course")
    search_fields = ("title", "description")
    ordering = ["order"]
    readonly_fields = ("created_at", "updated_at")

    actions = ["publish_projects", "unpublish_projects"]

    def publish_projects(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} project(s) published.")

    publish_projects.short_description = "Publish selected projects"

    def unpublish_projects(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} project(s) unpublished.")

    unpublish_projects.short_description = "Unpublish selected projects"

    def chapter_count(self, obj):
        return obj.chapters.count()

    chapter_count.short_description = "Chapters"

    def get_programming_languages(self, obj):
        return ", ".join([pl.name for pl in obj.programming_languages.all()])

    def get_framework(self, obj):
        return ", ".join([fw.name for fw in obj.framework.all()])

    get_programming_languages.short_description = "Languages"
    get_framework.short_description = "Frameworks"


class ChapterAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    inlines = [ChapterPartInline]
    list_display = ("title", "project", "order", "part_count")
    list_filter = ("project",)
    search_fields = ("title",)
    ordering = ["project", "order"]

    def part_count(self, obj):
        return obj.parts.count()

    part_count.short_description = "Parts"


class PartAdminForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = "__all__"
        widgets = {
            "description": SummernoteWidget(),
        }


class PartAdmin(admin.ModelAdmin):
    form = PartAdminForm
    list_display = ("title", "order")
    search_fields = ("title",)
    ordering = ["order"]


admin.site.register(Skill, SkillsAdmin)
admin.site.register(Framework, FrameworkAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(ProgrammingLanguage, ProgrammingLanguageAdmin)
admin.site.register(Difficulty)
admin.site.register(Stage, StagesAdmin)
admin.site.register(Review)
admin.site.register(Submission)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(ChapterPart)
admin.site.register(Course, CourseAdmin)
