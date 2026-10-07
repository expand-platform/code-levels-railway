from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_summernote.widgets import SummernoteWidget
from django import forms

from adminsortable2.admin import SortableAdminMixin

from platform_web.models.project.Course import CourseType
from platform_web.models.project.Project import Project
from platform_web.models.project.Skill import Skill


class SkillContentsWidget(SummernoteWidget):
    """Outline editor. Empty HTML is stored as ''."""

    @classmethod
    def compact(cls):
        return cls(
            attrs={
                "summernote": {
                    "width": 480,
                    "height": 180,
                    "toolbar": [],
                }
            }
        )

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return "" if value is None else value


class SkillAdminForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"
        widgets = {
            "contents": SkillContentsWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        projects_field = self.fields.get("projects")
        if not projects_field:
            return
        if self.instance.pk and self.instance.related_course_id:
            related_course = self.instance.related_course
            projects_qs = Project.objects.filter(is_active=True)
            if related_course.type != CourseType.JOB:
                projects_qs = projects_qs.filter(course_id=related_course.pk)
            else:
                projects_field.help_text = _(
                    "Projects can belong to any library course; they appear on this job track via this skill."
                )
            projects_field.queryset = projects_qs.order_by(
                "skill_order", "course_order", "title"
            )
        else:
            projects_field.queryset = Project.objects.filter(is_active=True)
            projects_field.help_text = _(
                "Save the skill with a course first, then assign projects."
            )


@admin.register(Skill)
class SkillsAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    form = SkillAdminForm
    list_display = ("order", "name", "related_course")
    list_filter = ("related_course",)
    search_fields = ("name",)
    ordering = ("order",)
    filter_horizontal = ("projects",)
    readonly_fields = ("uuid",)
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "name",
                    "related_course",
                    "projects",
                    "contents",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "order",
                    "uuid",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("related_course")
