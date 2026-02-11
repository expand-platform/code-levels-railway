import re
from django.forms import SlugField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from platform_web.models.app.project.Lesson import Lesson
import json

from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.Chapter import Chapter
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

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


def project_details_view(request: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(Project, slug=slug)
    start_url = None
    
    # You may want to generate the start_url for the first part of the project
    # For now, just link to the project parts view as a placeholder
    if project:
        start_url = f"/project/{project.slug}/parts/"
    parts = project.parts.all().order_by("order", "title")
    context = {
        "project": project,
        "start_url": start_url,
        "parts": parts,
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
    for idx, p in enumerate(parts):
        if p.order == part.order:
            if idx > 0:
                prev_part = parts[idx-1]
            if idx < len(parts)-1:
                next_part = parts[idx+1]
            break
    context = {
        "project": project,
        "part": part,
        "parts": parts,
        "prev_part": prev_part,
        "next_part": next_part,
        "user": request.user,
    }
    return render(request, "website/dashboard/pages/lesson_details.html", context)


@require_POST
@csrf_exempt
def reorder_lessons_view(request, slug):
    if not request.user.is_staff:
        return HttpResponse(status=403)
    try:
        data = json.loads(request.body)
        order_list = data.get('order', [])
        for item in order_list:
            lesson_id = item['id']
            new_order = item['order']
            Lesson.objects.filter(id=lesson_id, project__slug=slug).update(order=new_order)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type='application/json', status=400)


@require_POST
@csrf_exempt
def reorder_projects_by_language_view(request, language_id):
    if not request.user.is_staff:
        return HttpResponse(status=403)
    try:
        data = json.loads(request.body)
        order_list = data.get('order', [])
        language = ProgrammingLanguage.objects.get(id=language_id)
        for item in order_list:
            project_id = item['id']
            new_order = item['order']
            Project.objects.filter(id=project_id, programming_languages=language).update(language_order=new_order)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type='application/json', status=400)

@require_POST
@csrf_exempt
def reorder_projects_by_course_view(request, course_id):
    if not request.user.is_staff:
        return HttpResponse(status=403)
    try:
        data = json.loads(request.body)
        order_list = data.get('order', [])
        for item in order_list:
            project_id = item['id']
            new_order = item['order']
            Project.objects.filter(id=project_id, course_id=course_id).update(course_order=new_order)
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type='application/json', status=400)