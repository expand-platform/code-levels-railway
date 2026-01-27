from django.contrib import admin
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


class ChapterPartInline(admin.TabularInline):
    model = ChapterPart
    extra = 1
    fields = ("part", "custom_title", "order")
    autocomplete_fields = ["part"]
    ordering = ["order"]


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_programming_languages",
        "get_framework",
        "order",
        "difficulty",
        "is_active",
    )
    list_filter = ("is_active", "difficulty", "programming_languages", "framework")
    search_fields = ("title", "description")

    def get_programming_languages(self, obj):
        return ", ".join([pl.name for pl in obj.programming_languages.all()])

    def get_framework(self, obj):
        return ", ".join([fw.name for fw in obj.framework.all()])

    get_programming_languages.short_description = "Languages"
    get_framework.short_description = "Frameworks"


class ChapterAdmin(admin.ModelAdmin):
    inlines = [ChapterPartInline]
    list_display = ("title", "project", "order")
    list_filter = ("project",)
    search_fields = ("title",)
    ordering = ["project", "order"]


class PartAdmin(admin.ModelAdmin):
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
