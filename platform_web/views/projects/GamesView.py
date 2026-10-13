from django.db.models import Prefetch
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from platform_web.models.project.Course import Course
from platform_web.models.project.Game import Game


def _ordered_games():
    return Game.objects.order_by("order", "title")


class GamesView(TemplateView):
    template_name = "website/projects/pages/games.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = _ordered_games()
        context["courses"] = (
            Course.objects.filter(id__in=games.exclude(course_id=None).values("course_id"))
            .order_by("order", "title")
            .prefetch_related(Prefetch("games", queryset=_ordered_games()))
        )
        context["ungrouped_games"] = games.filter(course_id=None)
        context["page_title"] = _("Games")
        context["breadcrumbs"] = [
            {"label": _("Games"), "url": "", "active": True},
        ]
        context["show_content_filters"] = False
        return context
