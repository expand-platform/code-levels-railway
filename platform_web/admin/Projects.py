from django.contrib import admin
from django_summernote.widgets import SummernoteWidget
from django import forms

from adminsortable2.admin import SortableAdminMixin

from platform_web.admin.Lessons import LessonsInline
from platform_web.models.project.Course import Course, CourseType
from platform_web.models.project.Project import Project


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "description": SummernoteWidget(),
            "stages": SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        course_field = self.fields.get("course")
        if course_field:
            course_field.queryset = Course.objects.exclude(type=CourseType.JOB)


@admin.register(Project)
class ProjectAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    form = ProjectAdminForm
    inlines = [LessonsInline]
    changeform_format = "horizontal_tabs"
    list_display = (
        "course_order",
        "title",
        "course",
        "type",
        "get_programming_languages",
        "updated_at",
    )
    list_filter = ("type", "course")
    search_fields = ("title", "description")
    ordering = ("course_order",)
    readonly_fields = ("uuid", "created_at", "updated_at")
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "title",
                    "image",
                    "type",
                    "course",
                    "programming_languages",
                    "difficulty",
                    "framework",
                    "codepen_url",
                    "description",
                    "stages",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "is_active",
                    "is_video_course",
                    "language_order",
                    "course_order",
                    "skill_order",
                    "order",
                    "slug",
                    "uuid",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    actions = ["publish_projects", "unpublish_projects"]

    def publish_projects(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} project(s) published.")

    publish_projects.short_description = "Publish selected projects"  # type: ignore[attr-defined]

    def unpublish_projects(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} project(s) unpublished.")

    unpublish_projects.short_description = "Unpublish selected projects"  # type: ignore[attr-defined]

    def get_programming_languages(self, obj):
        return ", ".join([pl.name for pl in obj.programming_languages.all()])

    def get_framework(self, obj):
        return ", ".join([fw.name for fw in obj.framework.all()])

    get_programming_languages.short_description = "Languages"  # type: ignore[attr-defined]
    get_framework.short_description = "Frameworks"  # type: ignore[attr-defined]
