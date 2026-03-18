from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from platform_web.models.app.project.Course import Course
from platform_web.models.app.project.Lesson import Lesson
from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage



@login_required
def projects_view(request):
    default_filter = "course"
    default_project_type = "project"

    filter_by = request.GET.get("filter", default_filter)
    project_type = request.GET.get("type", default_project_type)
    search_query = request.GET.get("search", "").strip()

    context = {
        "filter_by": filter_by,
        "project_type": project_type,
        "search": search_query,
    }
    context_key = "courses"

    if filter_by == "course":
        items = Course.objects.prefetch_related("projects").order_by("order", "title")
        get_projects = lambda item: item.projects.order_by(
            "course_order", "order", "-updated_at", "title"
        )
    else:
        items = ProgrammingLanguage.objects.prefetch_related("project_set").order_by(
            "order", "name"
        )
        get_projects = lambda item: item.project_set.order_by(
            "language_order", "order", "-updated_at", "title"
        )
        context_key = "languages"

    for item in items:
        projects_qs = get_projects(item)
        if project_type != "all":
            projects_qs = projects_qs.filter(type=project_type)
        if search_query:
            projects_qs = projects_qs.filter(title__icontains=search_query)
        setattr(item, "filtered_projects", projects_qs)
    context[context_key] = items

    return render(request, "website/dashboard/pages/projects.html", context)


def project_details_view(request: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(Project, slug=slug)
    start_url = None
    if project:
        start_url = f"/project/{project.slug}/parts/"
    parts = project.parts.all().order_by("order", "title")

    # Filter projects and topics for this course
    filtered_projects = []
    filtered_topics = []
    if project.course:
        all_course_projects = project.course.projects.all().order_by("order", "title")
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


def lesson_details_view(request: HttpRequest, slug: str, order: int) -> HttpResponse:
    """
    Article-style view for a single project part, with navigation and sidebar.
    """
    project = get_object_or_404(Project, slug=slug)
    parts = list(project.parts.all().order_by("order", "title"))
    part = get_object_or_404(Lesson, project=project, order=order)
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
