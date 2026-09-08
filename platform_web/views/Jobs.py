from django.utils.translation import gettext_lazy as _

from .Roadmap import RoadmapView


class JobsView(RoadmapView):
    job_tracks_only = True
    page_title = _("Roadmap")
    list_url_name = "roadmap"
    detail_url_name = "roadmap_by_course"
    empty_message = _("No skills on the roadmap yet.")
