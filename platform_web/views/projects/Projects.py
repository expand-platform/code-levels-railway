from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext as _

from platform_web.models.project.Course import Course, CourseType
from platform_web.models.project.Lesson import Lesson
from platform_web.models.project.Project import Project, ProjectType
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage


MAX_SEARCH_LENGTH = 100
PROJECTS_LAYOUT_QUERY = "view"
PROJECTS_LAYOUT_DEFAULT = "default"
PROJECTS_LAYOUT_ROADMAP = "roadmap"
PROJECTS_CONTENT_QUERY = "content"
PROJECTS_CONTENT_CONCEPTS = "concepts"

MODE_SETTINGS = {
    "projects": {
        "filter_by": "course",
        "project_type": ProjectType.PROJECT,
        "is_video_course": "false",
    },
    "topics": {
        "filter_by": "language",
        "project_type": ProjectType.TOPIC,
        "is_video_course": "false",
    },
    "concepts": {
        "filter_by": "language",
        "project_type": ProjectType.CONCEPT,
        "is_video_course": None,
    },
    "courses": {
        "filter_by": "course",
        "project_type": ProjectType.PROJECT,
        "is_video_course": "true",
    },
}


def _list_page_titles(page_mode, project_type):
    """Return (page_title, breadcrumb_label) for the projects list page."""
    if page_mode == "courses":
        label = _("Courses")
        return label, label
    if project_type == "topic":
        label = _("Topics")
        return label, label
    if project_type == "concept":
        label = _("Concepts")
        return label, label
    if project_type == "all":
        return _("All Projects & Topics"), _("Projects & Topics")
    label = _("Projects")
    return label, label


def filter_by_workouts_toggle(projects_qs, show_workouts):
    """Show regular projects, plus workouts when the toggle is on."""
    if show_workouts:
        return projects_qs.filter(type__in=[ProjectType.PROJECT, ProjectType.WORKOUT])
    return projects_qs.filter(type=ProjectType.PROJECT)


def _apply_list_filters(
    projects_qs,
    *,
    page_mode,
    project_type,
    is_video_course,
    search_query,
    show_workouts,
):
    if page_mode == "projects":
        projects_qs = filter_by_workouts_toggle(projects_qs, show_workouts)
    elif project_type != "all":
        projects_qs = projects_qs.filter(type=project_type)

    if is_video_course == "true":
        projects_qs = projects_qs.filter(is_video_course=True)
    elif is_video_course == "false":
        projects_qs = projects_qs.filter(is_video_course=False)

    if search_query:
        # Search always targets projects only (workouts toggle is off while searching).
        projects_qs = projects_qs.filter(title__icontains=search_query)
        if page_mode == "projects":
            projects_qs = projects_qs.filter(type=ProjectType.PROJECT)

    return projects_qs


def _render_projects_page(
    request,
    page_mode="projects",
    selected_course_id=None,
    selected_language_id=None,
):
    mode_settings = MODE_SETTINGS.get(page_mode, MODE_SETTINGS["projects"])

    filter_by = mode_settings["filter_by"]
    project_type = mode_settings["project_type"]
    is_video_course = mode_settings["is_video_course"]
    search_query = request.GET.get("search", "").strip()[:MAX_SEARCH_LENGTH]
    show_workouts = (
        page_mode == "projects"
        and not search_query
        and request.GET.get("show_workouts") == "1"
    )
    # On projects list, reorder only when workouts are shown (mixed grid).
    can_reorder_projects = page_mode != "projects" or show_workouts
    page_title, breadcrumb_label = _list_page_titles(page_mode, project_type)

    context = {
        "page_mode": page_mode,
        "filter_by": filter_by,
        "project_type": project_type,
        "is_video_course": is_video_course,
        "search": search_query,
        "show_workouts": show_workouts,
        "can_reorder_projects": can_reorder_projects,
        "page_title": page_title,
        "breadcrumbs": [
            {"label": breadcrumb_label, "url": "", "active": True},
        ],
        "selected_course_id": selected_course_id,
        "selected_language_id": selected_language_id,
        "projects_layout": PROJECTS_LAYOUT_DEFAULT,
        "show_layout_toggle": page_mode == "projects",
        "show_content_filters": page_mode == "projects",
        "layout_query": "",
    }

    context_key = "courses"

    if filter_by == "course":
        items = (
            Course.objects.filter(type=CourseType.REGULAR)
            .prefetch_related("projects")
            .order_by("order", "title")
        )
        if selected_course_id is not None:
            items = items.filter(id=selected_course_id)

        def get_projects(item):
            return item.projects.select_related("difficulty").order_by(
                "course_order", "order", "-updated_at", "title"
            )
    else:
        items = ProgrammingLanguage.objects.prefetch_related("project_set").order_by(
            "order", "name"
        )
        if selected_language_id is not None:
            items = items.filter(id=selected_language_id)

        def get_projects(item):
            return item.project_set.select_related("difficulty").order_by(
                "language_order", "order", "-updated_at", "title"
            )

        context_key = "languages"

    visible_items = []
    for item in items:
        projects_qs = _apply_list_filters(
            get_projects(item).filter(is_active=True),
            page_mode=page_mode,
            project_type=project_type,
            is_video_course=is_video_course,
            search_query=search_query,
            show_workouts=show_workouts,
        )

        if context_key == "languages" and not projects_qs.exists():
            continue

        setattr(item, "filtered_projects", projects_qs)
        visible_items.append(item)
    context[context_key] = visible_items

    return render(request, "website/projects/pages/projects.html", context)


def projects_page_view(request, course_slug: str | None = None):
    show_grid = (
        request.GET.get(PROJECTS_LAYOUT_QUERY) == PROJECTS_LAYOUT_DEFAULT
        and request.GET.get(PROJECTS_CONTENT_QUERY) != PROJECTS_CONTENT_CONCEPTS
    )
    if not show_grid:
        from .Roadmap import RoadmapView

        kwargs = {}
        if course_slug:
            kwargs["course_slug"] = course_slug
        return RoadmapView.as_view()(request, **kwargs)
    if course_slug:
        return projects_by_course_view(request, course_slug)
    return projects_view(request)


def projects_view(request):
    return _render_projects_page(request, page_mode="projects")


def projects_by_course_view(request, course_slug: str):
    course = get_object_or_404(Course, slug=course_slug, type=CourseType.REGULAR)
    return _render_projects_page(
        request,
        page_mode="projects",
        selected_course_id=course.pk,
    )


def topics_view(request):
    return _render_projects_page(request, page_mode="topics")


def concepts_view(request):
    return _render_projects_page(request, page_mode="concepts")


def topics_by_language_view(request, language_slug: str):
    language = get_object_or_404(ProgrammingLanguage, slug=language_slug)
    return _render_projects_page(
        request,
        page_mode="topics",
        selected_language_id=language.pk,
    )


def courses_view(request):
    return _render_projects_page(request, page_mode="courses")


def courses_by_course_view(request, course_id: int):
    course = get_object_or_404(Course, pk=course_id, type=CourseType.REGULAR)
    return _render_projects_page(
        request,
        page_mode="courses",
        selected_course_id=course.pk,
    )


def project_details_view(request: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(Project, slug=slug, is_active=True)
    start_url = f"/projects/{project.slug}/parts/"
    parts = Lesson.objects.filter(project=project).order_by("order", "title")

    filtered_projects = []
    filtered_topics = []
    if project.course:
        all_course_projects = Project.objects.filter(
            course=project.course, is_active=True
        ).order_by("order", "title")
        filtered_projects = [
            p for p in all_course_projects if p.type == ProjectType.PROJECT
        ]
        filtered_topics = [
            p for p in all_course_projects if p.type == ProjectType.TOPIC
        ]

    context = {
        "project": project,
        "start_url": start_url,
        "parts": parts,
        "filtered_projects": filtered_projects,
        "filtered_topics": filtered_topics,
    }
    return render(request, "website/projects/pages/project_details.html", context)


def lesson_details_view(request: HttpRequest, slug: str, part_slug: str) -> HttpResponse:
    project = get_object_or_404(Project, slug=slug, is_active=True)
    parts = list(Lesson.objects.filter(project=project).order_by("order", "title"))
    part = get_object_or_404(Lesson, project=project, slug=part_slug)

    prev_part = next_part = None
    lesson_number = None
    for idx, p in enumerate(parts):
        if p.order == part.order:
            lesson_number = idx + 1
            if idx > 0:
                prev_part = parts[idx - 1]
            if idx < len(parts) - 1:
                next_part = parts[idx + 1]
            break

    context = {
        "project": project,
        "part": part,
        "parts": parts,
        "prev_part": prev_part,
        "next_part": next_part,
        "lesson_number": lesson_number,
        "user": request.user,
    }
    return render(request, "website/projects/pages/lesson_details.html", context)
