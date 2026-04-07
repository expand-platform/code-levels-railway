from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.conf import settings

from platform_web.models.app.project.Course import Course
from platform_web.models.app.project.Lesson import Lesson
from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage



def _render_projects_page(request, lang=None, page_mode="projects"):
    default_filter = "course"
    default_project_type = "project"
    default_video_filter = "all"
    max_search_length = 100
    is_courses_page = page_mode == "courses"

    filter_by = request.GET.get("filter", default_filter).strip().lower()
    project_type = request.GET.get("type", default_project_type).strip().lower()
    is_video_course = request.GET.get("is_video_course", default_video_filter).strip().lower()
    search_query = request.GET.get("search", "").strip()[:max_search_length]

    # Secure: restrict allowed values
    allowed_filters = {"course", "language"}
    allowed_project_types = {"project", "topic", "all"}
    allowed_video_filters = {"all", "true", "false"}
    
    if filter_by not in allowed_filters:
        filter_by = default_filter
    if project_type not in allowed_project_types:
        project_type = default_project_type
    if is_video_course not in allowed_video_filters:
        is_video_course = default_video_filter
    if is_courses_page:
        is_video_course = "true"

    # Validate lang against allowed values only
    allowed_langs = {"en", "ru"}
    if lang not in allowed_langs:
        request_lang = (getattr(request, "LANGUAGE_CODE", "") or "").split("-")[0]
        default_lang = (getattr(settings, "LANGUAGE_CODE", "en") or "en").split("-")[0]
        lang = request_lang if request_lang in allowed_langs else default_lang
        if lang not in allowed_langs:
            lang = "en"

    context = {
        "page_mode": page_mode,
        "filter_by": filter_by,
        "project_type": project_type,
        "is_video_course": is_video_course,
        "search": search_query,
        "current_lang": lang,
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
        if is_video_course == "true":
            projects_qs = projects_qs.filter(is_video_course=True)
        elif is_video_course == "false":
            projects_qs = projects_qs.filter(is_video_course=False)
        if search_query:
            projects_qs = projects_qs.filter(title__icontains=search_query)
        projects_qs = projects_qs.filter(language=lang)
        setattr(item, "filtered_projects", projects_qs)
    context[context_key] = items

    return render(request, "website/dashboard/pages/projects.html", context)


@login_required
def projects_view(request, lang=None):
    return _render_projects_page(request, lang=lang, page_mode="projects")


@login_required
def courses_view(request, lang=None):
    return _render_projects_page(request, lang=lang, page_mode="courses")


def project_details_view(request: HttpRequest, lang: str, slug: str) -> HttpResponse:
    allowed_langs = {"en", "ru"}
    if lang not in allowed_langs:
        lang = "en"

    project = get_object_or_404(Project, slug=slug, language=lang)
    start_url = None
    if project:
        start_url = f"/{lang}/projects/{project.slug}/parts/"
    parts = project.parts.all().order_by("order", "title")

    # Filter projects and topics for this course
    filtered_projects = []
    filtered_topics = []
    if project.course:
        all_course_projects = project.course.projects.filter(language=lang).order_by("order", "title")
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
        "current_lang": lang,
    }
    return render(request, "website/dashboard/pages/project_details.html", context)


def lesson_details_view(request: HttpRequest, lang: str, slug: str, order: int) -> HttpResponse:
    """
    Article-style view for a single project part, with navigation and sidebar.
    """
    allowed_langs = {"en", "ru"}
    if lang not in allowed_langs:
        lang = "en"

    project = get_object_or_404(Project, slug=slug, language=lang)
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
        "current_lang": lang,
    }
    return render(request, "website/dashboard/pages/lesson_details.html", context)
