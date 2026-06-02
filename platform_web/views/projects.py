from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from platform_web.models.project.Course import Course
from platform_web.models.project.Lesson import Lesson
from platform_web.models.project.Project import Project
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage

DEFAULT_FILTER = "course"
DEFAULT_PROJECT_TYPE = "project"
DEFAULT_VIDEO_FILTER = "all"
MAX_SEARCH_LENGTH = 100

def correct_get_filters(filter_by, project_type, is_video_course, is_courses_page=False):
    allowed_filters = {"course", "language"}
    allowed_project_types = {"project", "topic", "all"}
    allowed_video_filters = {"all", "true", "false"}
    
    if filter_by not in allowed_filters:
        filter_by = DEFAULT_FILTER
    if project_type not in allowed_project_types:
        project_type = DEFAULT_PROJECT_TYPE
    if is_video_course not in allowed_video_filters:
        is_video_course = DEFAULT_VIDEO_FILTER
    if is_courses_page:
        is_video_course = "true"
        
    return filter_by, project_type, is_video_course
    

def _render_projects_page(request, page_mode="projects"):
    IS_COURSES_PAGE = page_mode == "courses"

    filter_by = request.GET.get("filter", DEFAULT_FILTER).strip().lower()
    project_type = request.GET.get("type", DEFAULT_PROJECT_TYPE).strip().lower()
    is_video_course = request.GET.get("is_video_course", DEFAULT_VIDEO_FILTER).strip().lower()
    search_query = request.GET.get("search", "").strip()[:MAX_SEARCH_LENGTH]
    selected_course_raw = request.GET.get("course", "").strip()
    selected_course_id = None
    if selected_course_raw.isdigit():
        selected_course_id = int(selected_course_raw)

    selected_language_raw = request.GET.get("language", "").strip()
    selected_language_id = None
    if selected_language_raw.isdigit():
        selected_language_id = int(selected_language_raw)

    # Secure: restrict allowed values
    filter_by, project_type, is_video_course = correct_get_filters(
        filter_by, project_type, is_video_course, is_courses_page=IS_COURSES_PAGE
    )

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


def courses_view(request):
    return _render_projects_page(request, page_mode="courses")


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


def lesson_details_view(request: HttpRequest, slug: str, order: int) -> HttpResponse:
    """
    Article-style view for a single project part, with navigation and sidebar.
    """
    project = get_object_or_404(Project, slug=slug, is_active=True)
    parts = list(Lesson.objects.filter(project=project).order_by("order", "title"))
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
