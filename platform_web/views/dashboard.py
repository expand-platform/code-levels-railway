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
    filter_by = request.GET.get("filter", "language")
    project_type = request.GET.get("type", "all")
    context = {"filter_by": filter_by, "project_type": project_type}
    if filter_by == "course":
        courses = Course.objects.prefetch_related("projects").all()
        if project_type != "all":
            for course in courses:
                course.filtered_projects = course.projects.filter(type=project_type)
        else:
            for course in courses:
                course.filtered_projects = course.projects.all()
        context["courses"] = courses
    else:
        languages = ProgrammingLanguage.objects.prefetch_related("project_set").all()
        if project_type != "all":
            for language in languages:
                language.filtered_projects = language.project_set.filter(
                    type=project_type
                )
        else:
            for language in languages:
                language.filtered_projects = language.project_set.all()
        context["languages"] = languages
    return render(request, "website/dashboard/pages/projects.html", context)


class MapView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/map.html"


class LevelsView(LoginRequiredMixin, TemplateView):
    template_name = "website/dashboard/pages/levels.html"
