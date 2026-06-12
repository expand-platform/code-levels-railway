from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from platform_web.models.project.Course import Course
from platform_web.models.project.Lesson import Lesson
from platform_web.models.project.Project import Project
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage

from platform_web.decorators import paid_plans_only


MAX_SEARCH_LENGTH = 100

MODE_SETTINGS = {
    "projects": {
        "filter_by": "course",
        "project_type": "project",
        "is_video_course": "false",
    },
    "topics": {
        "filter_by": "language",
        "project_type": "topic",
        "is_video_course": "false",
    },
    "courses": {
        "filter_by": "course",
        "project_type": "project",
        "is_video_course": "true",
    },
}


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

    context = {
        "page_mode": page_mode,
        "filter_by": filter_by,
        "project_type": project_type,
        "is_video_course": is_video_course,
        "search": search_query,
        "selected_course_id": selected_course_id,
        "selected_language_id": selected_language_id,
    }
    
    context_key = "courses"

    if filter_by == "course":
        items = Course.objects.prefetch_related("projects").order_by("order", "title")
        if selected_course_id is not None:
            items = items.filter(id=selected_course_id)
        get_projects = lambda item: item.projects.order_by(
            "course_order", "order", "-updated_at", "title"
        )
    # filter by language
    else:
        items = ProgrammingLanguage.objects.prefetch_related("project_set").order_by(
            "order", "name"
        )
        if selected_language_id is not None:
            items = items.filter(id=selected_language_id)
        get_projects = lambda item: item.project_set.order_by(
            "language_order", "order", "-updated_at", "title"
        )
        context_key = "languages"

    visible_items = []
    for item in items:
        projects_qs = get_projects(item).filter(is_active=True)
        
        if project_type != "all":
            projects_qs = projects_qs.filter(type=project_type)
        if is_video_course == "true":
            projects_qs = projects_qs.filter(is_video_course=True)
        elif is_video_course == "false":
            projects_qs = projects_qs.filter(is_video_course=False)
        if search_query:
            projects_qs = projects_qs.filter(title__icontains=search_query)

        # In language mode, hide blocks that have no matching projects.
        if context_key == "languages" and not projects_qs.exists():
            continue

        setattr(item, "filtered_projects", projects_qs)
        visible_items.append(item)
    context[context_key] = visible_items

    return render(request, "website/dashboard/pages/projects.html", context)


def projects_view(request):
    return _render_projects_page(request, page_mode="projects")


def projects_by_course_view(request, course_slug: str):
    course = get_object_or_404(Course, slug=course_slug)
    return _render_projects_page(
        request,
        page_mode="projects",
        selected_course_id=course.pk,
    )

def topics_view(request):
    return _render_projects_page(request, page_mode="topics")


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
    return _render_projects_page(
        request,
        page_mode="courses",
        selected_course_id=course_id,
    )


def project_details_view(request: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(Project, slug=slug, is_active=True)
    start_url = None
    if project:
        start_url = f"/projects/{project.slug}/parts/"
    parts = Lesson.objects.filter(project=project).order_by("order", "title")

    # Filter projects and topics for this course
    filtered_projects = []
    filtered_topics = []
    if project.course:
        all_course_projects = Project.objects.filter(
            course=project.course, is_active=True
        ).order_by("order", "title")
        filtered_projects = [
            p for p in all_course_projects if getattr(p, "type", None) == "project"
        ]
        filtered_topics = [
            p for p in all_course_projects if getattr(p, "type", None) == "topic"
        ]

    context = {
        "project": project,
        "start_url": start_url,
        "parts": parts,
        "filtered_projects": filtered_projects,
        "filtered_topics": filtered_topics,
    }
    return render(request, "website/dashboard/pages/project_details.html", context)


def lesson_details_view(request: HttpRequest, slug: str, part_slug: str) -> HttpResponse:
    """
    Article-style view for a single project part, with navigation and sidebar.
    """
    project = get_object_or_404(Project, slug=slug, is_active=True)
    parts = list(Lesson.objects.filter(project=project).order_by("order", "title"))
    part = get_object_or_404(Lesson, project=project, slug=part_slug)
    # Find prev/next part
    prev_part = next_part = None
    lesson_number = None
    for idx, p in enumerate(parts):
        if p.order == part.order:
            lesson_number = idx + 1  # 1-based index for display
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
    return render(request, "website/dashboard/pages/lesson_details.html", context)
