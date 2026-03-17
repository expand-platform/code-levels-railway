from django.contrib import admin
from django_summernote.widgets import SummernoteWidget
from django import forms

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from platform_web.models.app.project.Course import Course
from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.Lesson import Lesson
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Difficulty import Difficulty
from platform_web.models.app.project.Framework import Framework


class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("order", "title")
    search_fields = ("title",)


class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class StagesAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class LessonsInline(SortableInlineAdminMixin, NestedTabularInline):
    model = Lesson
    extra = 1
    fields = ("title", "order", "description", "languages")
    autocomplete_fields = ["languages"]
    ordering = ["order"]


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "description": SummernoteWidget(),
        }


class ProjectAdmin(SortableAdminMixin, NestedModelAdmin):  # type: ignore[misc]
    form = ProjectAdminForm
    inlines = [LessonsInline]
    list_display = (
        # "order",
        "course_order",
        "title",
        "course",
        "type",
        "get_programming_languages",
        "updated_at",
    )
    list_filter = ("difficulty", "programming_languages", "framework", "type", "course")
    search_fields = ("title", "description")
    ordering = ("course_order",)
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

    def get_programming_languages(self, obj):
        return ", ".join([pl.name for pl in obj.programming_languages.all()])

    def get_framework(self, obj):
        return ", ".join([fw.name for fw in obj.framework.all()])

    get_programming_languages.short_description = "Languages"
    get_framework.short_description = "Frameworks"


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
        widgets = {
            "description": SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Only for new Lesson
            latest_project = Project.objects.order_by('-id').first()
            if latest_project:
                self.fields['project'].initial = latest_project


class LessonsAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    form = LessonAdminForm
    list_display = ("order", "title", "type", "project", "last_edited")
    search_fields = ("title", "project__title")
    list_filter = ("project",)
    ordering = ("order",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("order")


class SkillsAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class DifficultiesAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("order", "name")


class FrameworkAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("order", "name")
    search_fields = ("name",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Difficulty, DifficultiesAdmin)

admin.site.register(ProgrammingLanguage, ProgrammingLanguageAdmin)
admin.site.register(Framework, FrameworkAdmin)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Lesson, LessonsAdmin)
