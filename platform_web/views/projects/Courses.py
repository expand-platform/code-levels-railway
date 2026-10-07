from django.db.models import Count
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from platform_web.models.project.Course import Course, CourseType


# type, heading, detail url name, link only when the course has a skill
COURSE_SECTIONS = (
    (CourseType.LANGUAGE, _("Language courses"), "roadmaps_by_course", False),
    (CourseType.REGULAR, _("Regular courses"), "projects_by_course", True),
    (CourseType.JOB, _("Job courses"), "job_tracks_by_course", True),
)


class CoursesView(TemplateView):
    template_name = "website/projects/pages/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_type_filter = self.request.GET.get("type", "")
        if course_type_filter not in {
            CourseType.LANGUAGE,
            CourseType.REGULAR,
            CourseType.JOB,
        }:
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
        context["course_type_filters"] = _course_type_filters()
        return context


def _course_sections():
    grouped, other = _group_courses()
    sections = []
    for course_type, title, url_name, needs_skills in COURSE_SECTIONS:
        _add_section(
            sections, title, grouped[course_type], url_name, needs_skills, course_type
        )
    _add_section(sections, _("Other"), other, "", False, "")
    return sections


def _group_courses():
    grouped = {section[0]: [] for section in COURSE_SECTIONS}
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


def _course_type_filters():
    return (
        ("", _("All")),
        (CourseType.LANGUAGE, _("Language")),
        (CourseType.REGULAR, _("Regular")),
        (CourseType.JOB, _("Job")),
    )


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
