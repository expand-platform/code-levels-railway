from django.utils.translation import gettext_lazy as _

from platform_web.models.project.Course import CourseType


class CourseSection:
    def __init__(self, course_type, heading, filter_label, url_name, needs_skills):
        self.type = course_type
        self.heading = heading
        self.filter_label = filter_label
        self.url_name = url_name
        self.needs_skills = needs_skills


class CoursesConfig:
    """Catalog sections for /courses/. Headings and filter labels stay in one list."""

    SECTIONS = (
        CourseSection(
            CourseType.LANGUAGE,
            _("Roadmaps"),
            _("Roadmap"),
            "roadmaps_by_course",
            False,
        ),
        CourseSection(
            CourseType.REGULAR,
            _("Regular courses"),
            _("Regular"),
            "projects_by_course",
            True,
        ),
        CourseSection(
            CourseType.JOB,
            _("Job courses"),
            _("Job"),
            "job_tracks_by_course",
            True,
        ),
    )

    @classmethod
    def valid_types(cls):
        return frozenset(section.type for section in cls.SECTIONS)

    @classmethod
    def type_filters(cls):
        return (("", _("All")),) + tuple(
            (section.type, section.filter_label) for section in cls.SECTIONS
        )
