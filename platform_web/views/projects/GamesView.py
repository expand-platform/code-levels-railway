from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from platform_web.models.project.Game import Game


class GamesView(TemplateView):
    template_name = "website/projects/pages/games.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Game.objects.all()
        context["page_title"] = _("Games")
        context["breadcrumbs"] = [
            {"label": _("Games"), "url": "", "active": True},
        ]
        context["show_layout_toggle"] = False
        context["show_content_filters"] = False
        return context
