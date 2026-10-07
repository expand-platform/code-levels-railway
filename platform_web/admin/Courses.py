from django.contrib import admin
from django import forms
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin

from platform_web.admin.Skills import SkillContentsWidget
from platform_web.models.project.Course import Course
from platform_web.models.project.Project import Project
from platform_web.models.project.Skill import Skill


class SkillInlineForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ("name", "order", "contents")
        widgets = {
            "contents": SkillContentsWidget.compact(),
        }


class SkillsInline(SortableInlineAdminMixin, admin.TabularInline):  # type: ignore[misc]
    model = Skill
    form = SkillInlineForm
    extra = 1
    fields = ("name", "order", "contents")
    ordering = ["order"]
    show_change_link = True


def _projects_table(projects, *, order_field, include_course=False):
    headers = [_("#"), _("Title"), _("Type"), _("Active")]

    if include_course:
        headers.append(_("Course"))

    rows = []

    for project in projects:
        cells = [
            getattr(project, order_field),
            format_html(
                '<a href="{}">{}</a>',
                reverse("admin:platform_web_project_change", args=[project.pk]),
                project.title,
            ),
            project.get_type_display(),
            _("Yes") if project.is_active else _("No"),
        ]

        if include_course:
            cells.append(project.course.title if project.course_id else "—")
        rows.append(format_html_join("", "<td>{}</td>", ((cell,) for cell in cells)))

    return format_html(
        '<table class="table table-sm table-striped course-related-projects">'
        "<thead><tr>{}</tr></thead><tbody>{}</tbody></table>",
        format_html_join("", "<th>{}</th>", ((header,) for header in headers)),
        mark_safe("".join(format_html("<tr>{}</tr>", row) for row in rows)),
    )


@admin.register(Course)
class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    changeform_format = "horizontal_tabs"
    jazzmin_section_order = (
        "General",
        "Skills",
        "Projects by course",
        "Projects by skills",
    )
    list_display = ("order", "title", "type")
    list_filter = ("type",)
    search_fields = ("title",)
    inlines = [SkillsInline]
    readonly_fields = ("uuid", "projects_by_course", "projects_by_skills")

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (
                "General",
                {
                    "fields": (
                        "title",
                        "image",
                        "description",
                        "slug",
                        "languages",
                        "type",
                        "order",
                        "uuid",
                    )
                },
            )
        ]
        if obj is None:
            return fieldsets

        if obj.projects.exists():
            fieldsets.append(
                ("Projects by course", {"fields": ("projects_by_course",)})
            )
        
        if Project.objects.filter(skills__related_course=obj).exists():
            fieldsets.append(
                ("Projects by skills", {"fields": ("projects_by_skills",)})
            )
        
        return fieldsets

    def projects_by_course(self, obj):
        projects = obj.projects.order_by("course_order", "order", "title")
        return _projects_table(projects, order_field="course_order")

    projects_by_course.short_description = ""  # type: ignore[attr-defined]

    def projects_by_skills(self, obj):
        skills = obj.skills.prefetch_related(
            Prefetch(
                "projects",
                queryset=Project.objects.select_related("course").order_by(
                    "skill_order", "course_order", "title"
                ),
            )
        ).order_by("order", "name")
        
        blocks = []
        
        for skill in skills:
            projects = list(skill.projects.all())
            
            if not projects:
                continue
            
            blocks.append(
                format_html(
                    '<div class="course-skill-projects">'
                    '<h4><a href="{}">{}</a></h4>{}</div>',
                    reverse("admin:platform_web_skill_change", args=[skill.pk]),
                    skill.name,
                    _projects_table(
                        projects,
                        order_field="skill_order",
                    ),
                )
            )
        return mark_safe("".join(blocks))

    projects_by_skills.short_description = ""  # type: ignore[attr-defined]
