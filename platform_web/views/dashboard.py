from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/dashboard.html"


@login_required
def projects_view(request):
    languages = ProgrammingLanguage.objects.prefetch_related('project_set').all()
    return render(request, 'website/dashboard/pages/projects.html', {'languages': languages})


class MapView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/map.html"


class LevelsView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/levels.html"
