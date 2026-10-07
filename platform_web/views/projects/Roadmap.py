from django.db.models import Exists, OuterRef, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from platform_web.models.project.Course import Course, CourseType
from platform_web.models.project.Project import Project
from platform_web.models.project.Skill import Skill
from .Projects import (
    PROJECTS_LAYOUT_QUERY,
    PROJECTS_LAYOUT_ROADMAP,
    filter_by_workouts_toggle,
)


class RoadmapView(TemplateView):
    template_name = "website/projects/pages/roadmap.html"
    course_type = CourseType.REGULAR
    include_courses_without_skills = False
    include_empty_skill_tracks = False
    show_layout_toggle = True
    show_workouts_by_default = False
    page_title = _("Projects")
    list_url_name = "projects"
    detail_url_name = "projects_by_course"
    empty_message = _("No skills yet.")

    def get_courses_queryset(self):
        courses = Course.objects.filter(type=self.course_type)
        if not self.include_courses_without_skills:
            courses = courses.filter(skills__isnull=False).distinct()
        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workouts_default = "1" if self.show_workouts_by_default else "0"
        show_workouts = self.request.GET.get("show_workouts", workouts_default) == "1"
        concepts_only = self.request.GET.get("content") == "concepts"
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
        has_projects = Exists(
            Skill.projects.through.objects.filter(skill_id=OuterRef("pk"))
        )
        skills = Skill.objects.annotate(has_projects=has_projects).order_by(
            "order", "name"
        )
        if not concepts_only and not self.include_empty_skill_tracks:
            skills = skills.filter(
                Q(pk__in=Skill.objects.filter(projects__in=active_projects).values("pk"))
                | (Q(has_projects=False) & ~Q(contents=""))
            )
        if not concepts_only:
            skills = skills.prefetch_related(
                Prefetch("projects", queryset=active_projects)
            )
        courses = courses.prefetch_related(
            Prefetch("skills", queryset=skills)
        ).order_by("order", "title")
        context["page_title"] = self.page_title
        context["list_url_name"] = self.list_url_name
        context["detail_url_name"] = self.detail_url_name
        context["empty_message"] = self.empty_message
        context["show_workouts"] = show_workouts
        context["can_reorder_projects"] = show_workouts
        context["selected_course"] = selected_course
        context["page_mode"] = "projects" if self.show_layout_toggle else None
        context["projects_layout"] = PROJECTS_LAYOUT_ROADMAP
        context["show_layout_toggle"] = self.show_layout_toggle
        context["show_content_filters"] = True
        context["concepts_only"] = concepts_only
        query = []
        if self.show_layout_toggle:
            query.append(f"{PROJECTS_LAYOUT_QUERY}={PROJECTS_LAYOUT_ROADMAP}")
        if concepts_only:
            query.append("content=concepts")
        context["layout_query"] = f"?{'&'.join(query)}" if query else ""
        if self.include_empty_skill_tracks:
            context["courses"] = courses
        else:
            context["courses"] = [
                course for course in courses if course.skills.all()
            ]
        return context
