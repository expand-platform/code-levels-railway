from django.db.models import Exists, OuterRef, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from platform_web.config.models.ProjectConfig import ProjectConfig
from platform_web.models.project.Course import Course, CourseType
from platform_web.models.project.Project import Project
from platform_web.models.project.Skill import Skill
from .Projects import filter_by_workouts_toggle


class RoadmapView(TemplateView):
    template_name = "website/projects/pages/roadmap.html"
    course_type = CourseType.REGULAR
    include_courses_without_skills = False
    include_empty_skill_tracks = False
    layout_kind = ProjectConfig.LAYOUT_PROJECTS
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
        if not self.include_empty_skill_tracks:
            skills = skills.filter(
                Q(pk__in=Skill.objects.filter(projects__in=active_projects).values("pk"))
                | (Q(has_projects=False) & ~Q(contents=""))
            )
        skills = skills.prefetch_related(
            Prefetch("projects", queryset=active_projects)
        )
        courses = courses.prefetch_related(
            Prefetch("skills", queryset=skills)
        ).order_by("order", "title")
        context["page_title"] = self.page_title
        context["empty_message"] = self.empty_message
        context["show_workouts"] = show_workouts
        context["can_reorder_projects"] = show_workouts
        current_layout, layout_query = self._layout()
        context["page_mode"] = (
            "projects" if self.layout_kind == ProjectConfig.LAYOUT_PROJECTS else None
        )
        context["layout_toggle"] = ProjectConfig.layout_toggle(
            self.layout_kind, current_layout
        )
        context["hide_skill_contents"] = (
            current_layout == ProjectConfig.ROADMAP_LAYOUT_LIST
        )
        context["show_content_filters"] = True
        context["breadcrumbs"] = _breadcrumbs(
            self.page_title,
            self.list_url_name,
            self.detail_url_name,
            selected_course,
            layout_query,
        )
        if self.include_empty_skill_tracks:
            context["courses"] = courses
        else:
            context["courses"] = [
                course for course in courses if course.skills.all()
            ]
        return context

    def _layout(self):
        if self.layout_kind == ProjectConfig.LAYOUT_ROADMAP:
            current = ProjectConfig.roadmap_layout(self.request.GET)
            default = ProjectConfig.PROJECTS_LAYOUT_ROADMAP
        elif self.layout_kind == ProjectConfig.LAYOUT_PROJECTS:
            current = ProjectConfig.PROJECTS_LAYOUT_ROADMAP
            default = ProjectConfig.PROJECTS_LAYOUT_DEFAULT
        else:
            return "", ""
        return current, ProjectConfig.view_query(current, default=default)


def _breadcrumbs(page_title, list_url_name, detail_url_name, selected_course, layout_query):
    crumbs = [
        {
            "label": page_title,
            "url": reverse(list_url_name) + layout_query,
            "active": selected_course is None,
        }
    ]
    if selected_course:
        crumbs.append(
            {
                "label": selected_course.title,
                "url": reverse(detail_url_name, args=[selected_course.slug]) + layout_query,
                "active": True,
            }
        )
    return crumbs
