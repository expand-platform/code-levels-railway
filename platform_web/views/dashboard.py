from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Course import Course

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/dashboard.html"


@login_required
def projects_view(request):
    default_filter = "course"
    default_project_type = "project"

    filter_by = request.GET.get("filter", default_filter)
    project_type = request.GET.get("type", default_project_type)

    context = {"filter_by": filter_by, "project_type": project_type}
    context_key = "courses"

    if filter_by == "course":
        items = Course.objects.prefetch_related("projects").order_by("order", "title")
        get_projects = lambda item: item.projects.order_by("course_order", "order", "-updated_at", "title")
    else:
        items = ProgrammingLanguage.objects.prefetch_related("project_set").order_by("order", "name")
        get_projects = lambda item: item.project_set.order_by("language_order", "order", "-updated_at", "title")
        context_key = "languages"

    for item in items:
        if project_type != "all":
            setattr(item, 'filtered_projects', get_projects(item).filter(type=project_type))
        else:
            setattr(item, 'filtered_projects', get_projects(item))
    context[context_key] = items

    return render(request, "website/dashboard/pages/projects.html", context)


class MapView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/map.html"


class LevelsView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/levels.html"
