from django.utils.translation import gettext_lazy as _

from platform_web.models.project.Course import CourseType

from .Roadmap import RoadmapView


class LanguagesView(RoadmapView):
    course_type = CourseType.LANGUAGE
    include_courses_without_skills = True
    include_empty_skill_tracks = True
    show_layout_toggle = False
    page_title = _("Languages")
    list_url_name = "languages"
    detail_url_name = "languages_by_course"
    empty_message = _("No skills yet.")
