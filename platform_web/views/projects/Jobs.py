from django.utils.translation import gettext_lazy as _

from platform_web.config.ProjectConfig import ProjectConfig
from platform_web.models.project.Course import CourseType

from .Roadmap import RoadmapView


class JobsView(RoadmapView):
    course_type = CourseType.JOB
    include_empty_skill_tracks = True
    layout_kind = ProjectConfig.LAYOUT_NONE
    show_workouts_by_default = True
    page_title = _("Roadmap")
    list_url_name = "job_tracks"
    detail_url_name = "job_tracks_by_course"
    empty_message = _("No skills on the roadmap yet.")
