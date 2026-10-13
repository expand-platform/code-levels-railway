from django.db.models import Count
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from platform_web.config.CoursesConfig import CoursesConfig
from platform_web.models.project.Course import Course


class CoursesView(TemplateView):
    template_name = "website/projects/pages/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_type_filter = self.request.GET.get("type", "")
        if course_type_filter not in CoursesConfig.valid_types():
            course_type_filter = ""
        sections = _course_sections()
        if course_type_filter:
            sections = [
                section
                for section in sections
                if section["type"] == course_type_filter
            ]
        context["sections"] = sections
        context["page_title"] = _("Courses")
        context["breadcrumbs"] = [
            {"label": _("Courses"), "url": "", "active": True},
        ]
        context["show_course_filters"] = True
        context["course_type_filter"] = course_type_filter
        context["course_type_filters"] = CoursesConfig.type_filters()
        return context


def _course_sections():
    grouped, other = _group_courses()
    sections = []
    for section in CoursesConfig.SECTIONS:
        _add_section(
            sections,
            section.heading,
            grouped[section.type],
            section.url_name,
            section.needs_skills,
            section.type,
        )
    _add_section(sections, _("Other"), other, "", False, "")
    return sections


def _group_courses():
    grouped = {section.type: [] for section in CoursesConfig.SECTIONS}
    other = []
    courses = Course.objects.annotate(skill_count=Count("skills")).order_by(
        "order", "title"
    )
    for course in courses:
        bucket = grouped.get(course.type)
        if bucket is None:
            other.append(course)
        else:
            bucket.append(course)
    return grouped, other


def _add_section(sections, title, courses, url_name, needs_skills, course_type):
    if not courses:
        return
    for course in courses:
        course.detail_url = _detail_url(course, url_name, needs_skills)
    courses.sort(key=lambda course: course.detail_url == "")
    sections.append({"title": title, "courses": courses, "type": course_type})


def _detail_url(course, url_name, needs_skills):
    if url_name and course.slug and (not needs_skills or course.skill_count):
        return reverse(url_name, args=[course.slug])
    return ""
