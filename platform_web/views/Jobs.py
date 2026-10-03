from django.utils.translation import gettext_lazy as _

from platform_web.models.project.Course import CourseType

from .Roadmap import RoadmapView


class JobsView(RoadmapView):
    course_type = CourseType.JOB
    include_empty_skill_tracks = True
    show_layout_toggle = False
    page_title = _("Roadmap")
    list_url_name = "roadmap"
    detail_url_name = "roadmap_by_course"
    empty_message = _("No skills on the roadmap yet.")
