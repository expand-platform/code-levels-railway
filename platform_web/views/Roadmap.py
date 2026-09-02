from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from platform_web.models.project.Course import Course
from platform_web.models.project.Project import Project
from platform_web.models.project.Skill import Skill
from .Projects import filter_by_workouts_toggle


class RoadmapView(TemplateView):
    template_name = "website/dashboard/pages/roadmap.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_workouts = self.request.GET.get("show_workouts") == "1"
        course_slug = self.kwargs.get("course_slug")
        active_projects = filter_by_workouts_toggle(
            Project.objects.filter(is_active=True).select_related("difficulty"),
            show_workouts,
        ).order_by("skill_order", "course_order", "title")
        courses = Course.objects.filter(skills__isnull=False).distinct()
        selected_course = None
        if course_slug:
            selected_course = get_object_or_404(courses, slug=course_slug)
            courses = courses.filter(pk=selected_course.pk)
        context["show_workouts"] = show_workouts
        context["can_reorder_projects"] = show_workouts
        context["selected_course"] = selected_course
        context["courses"] = courses.prefetch_related(
            Prefetch(
                "skills",
                queryset=Skill.objects.order_by("order", "name").prefetch_related(
                    Prefetch("projects", queryset=active_projects)
                ),
            )
        ).order_by("order", "title")
        return context
