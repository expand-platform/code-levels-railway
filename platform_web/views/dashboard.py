from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/dashboard.html"



from platform_web.models.app.project.Course import Course

@login_required
def projects_view(request):
    filter_by = request.GET.get('filter', 'language')
    context = {'filter_by': filter_by}
    if filter_by == 'course':
        courses = Course.objects.prefetch_related('projects').all()
        context['courses'] = courses
    else:
        languages = ProgrammingLanguage.objects.prefetch_related('project_set').all()
        context['languages'] = languages
    return render(request, 'website/dashboard/pages/projects.html', context)


class MapView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/map.html"


class LevelsView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/levels.html"
