from django.utils.translation import gettext_lazy as _

from platform_web.models.project.Course import CourseType

from .Roadmap import RoadmapView


class RoadmapsView(RoadmapView):
    course_type = CourseType.LANGUAGE
    include_courses_without_skills = True
    include_empty_skill_tracks = True
    show_layout_toggle = False
    show_workouts_by_default = True
    page_title = _("Roadmaps")
    list_url_name = "roadmaps"
    detail_url_name = "roadmaps_by_course"
    empty_message = _("No skills yet.")
