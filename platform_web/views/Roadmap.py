from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from platform_web.models.project.Course import Course
from platform_web.models.project.Project import Project
from platform_web.models.project.Skill import Skill
from .Projects import (
    PROJECTS_LAYOUT_QUERY,
    PROJECTS_LAYOUT_ROADMAP,
    filter_by_workouts_toggle,
)


class RoadmapView(TemplateView):
    template_name = "website/dashboard/pages/roadmap.html"
    job_tracks_only = False
    page_title = _("Projects")
    list_url_name = "projects"
    detail_url_name = "projects_by_course"
    empty_message = _("No skills yet.")

    def get_courses_queryset(self):
        courses = Course.objects.filter(skills__isnull=False)
        if self.job_tracks_only:
            return courses.filter(is_job_course=True).distinct()
        return courses.filter(is_job_course=False).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_workouts = self.request.GET.get("show_workouts", "1") == "1"
        course_slug = self.kwargs.get("course_slug")
        active_projects = filter_by_workouts_toggle(
            Project.objects.filter(is_active=True).select_related("difficulty"),
            show_workouts,
        ).order_by("skill_order", "course_order", "title")
        courses = self.get_courses_queryset()
        selected_course = None
        if course_slug:
            selected_course = get_object_or_404(courses, slug=course_slug)
            courses = courses.filter(pk=selected_course.pk)
        skills_with_projects = (
            Skill.objects.filter(projects__in=active_projects)
            .distinct()
            .order_by("order", "name")
            .prefetch_related(Prefetch("projects", queryset=active_projects))
        )
        courses = courses.prefetch_related(
            Prefetch("skills", queryset=skills_with_projects)
        ).order_by("order", "title")
        show_layout_toggle = not self.job_tracks_only
        context["page_title"] = self.page_title
        context["list_url_name"] = self.list_url_name
        context["detail_url_name"] = self.detail_url_name
        context["empty_message"] = self.empty_message
        context["show_workouts"] = show_workouts
        context["can_reorder_projects"] = show_workouts
        context["selected_course"] = selected_course
        context["page_mode"] = "projects" if show_layout_toggle else None
        context["projects_layout"] = PROJECTS_LAYOUT_ROADMAP
        context["show_layout_toggle"] = show_layout_toggle
        context["layout_query"] = (
            f"?{PROJECTS_LAYOUT_QUERY}={PROJECTS_LAYOUT_ROADMAP}"
            if show_layout_toggle
            else ""
        )
        context["courses"] = [
            course for course in courses if len(course.skills.all())
        ]
        return context
