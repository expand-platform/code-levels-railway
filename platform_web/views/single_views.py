import re
from django.forms import SlugField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.Chapter import Chapter
from platform_web.models.app.project.Part import Part


def project_parts_view(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Shows all chapters and their ordered parts for a given project.
    """
    project = get_object_or_404(Project, slug=slug)
    chapters = Chapter.objects.filter(project=project).order_by("order", "title")
    chapter_data = []
    for chapter in chapters:
        parts = chapter.parts.all().order_by("order")
        chapter_data.append(
            {
                "chapter": chapter,
                "parts": parts,
            }
        )
    return render(
        request,
        "website/project/parts_view.html",
        {
            "project": project,
            "chapter_data": chapter_data,
        },
    )


def part_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    part = get_object_or_404(Part, pk=pk)
    codepen_hash = ""
    codepen_user = ""
    if part.codepen_url:
        # Example: https://codepen.io/ca-tt/pen/ExEENaZ
        hash_match = re.search(r"/pen/([a-zA-Z0-9]+)", part.codepen_url)
        user_match = re.search(r"codepen.io/([^/]+)/pen/", part.codepen_url)
        if hash_match:
            codepen_hash = hash_match.group(1)
        if user_match:
            codepen_user = user_match.group(1)
    context = {
        "part": part,
        "lesson_id": part.pk,
        "lesson_title": part.title,
        "lesson_description": part.description,
        "codepen_hash": codepen_hash,
        "codepen_user": codepen_user,
    }
    return render(request, "website/dashboard/pages/part.html", context)


def project_details_view(request: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(Project, slug=slug)
    start_url = None
    # You may want to generate the start_url for the first part of the project
    # For now, just link to the project parts view as a placeholder
    if project:
        start_url = f"/project/{project.slug}/parts/"
    context = {
        "project": project,
        "start_url": start_url,
        "website_config": getattr(request, 'website_config', None),
    }
    return render(request, "website/dashboard/pages/project_details.html", context)
