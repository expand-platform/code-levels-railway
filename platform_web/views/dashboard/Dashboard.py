from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from platform_web.models.project.Project import Project, ProjectType


RECOMMENDATION_LIMIT = 4


def _recommended(project_type):
    return Project.objects.filter(is_active=True, type=project_type).order_by("-updated_at")[
        :RECOMMENDATION_LIMIT
    ]


def _recommendation_column(heading, project_type, url_name, empty):
    return {
        "heading": heading,
        "items": _recommended(project_type),
        "see_all_url": reverse(url_name),
        "empty": empty,
    }


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["see_all"] = _("See all")
        context["recommendations"] = [
            _recommendation_column(
                _("Projects"), ProjectType.PROJECT, "projects", _("No projects yet.")
            ),
            _recommendation_column(
                _("Topics"), ProjectType.TOPIC, "topics", _("No topics yet.")
            ),
            _recommendation_column(
                _("Concepts"), ProjectType.CONCEPT, "concepts", _("No concepts yet.")
            ),
        ]
        return context


class DashboardPaymentView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/payment.html"


class DashboardChatView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/chat.html"
