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
    context = {
        "part": part,
        "lesson_id": part.pk,
        "lesson_title": part.title,
        "lesson_description": part.description,
        # Add more context as needed
    }
    return render(request, "website/dashboard/pages/part.html", context)
