from django.contrib import admin
from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.ProjectPart import ProjectPart
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Difficulty import Difficulty
from platform_web.models.app.project.DevelopmentStage import DevelopmentStage
from platform_web.models.app.project.Skill import Skill
from platform_web.models.app.project.Review import Review
from platform_web.models.app.project.Submission import Submission
from platform_web.models.app.learning_models import *


class ProjectPartInline(admin.TabularInline):
    model = ProjectPart
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectPartInline]
    list_display = ("title", "order", "is_active", "difficulty")
    list_filter = ("is_active", "difficulty", "programming_languages")
    search_fields = ("title", "description")


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectPart)
admin.site.register(ProgrammingLanguage)
admin.site.register(Difficulty)
admin.site.register(DevelopmentStage)
admin.site.register(Skill)
admin.site.register(Review)
admin.site.register(Submission)
