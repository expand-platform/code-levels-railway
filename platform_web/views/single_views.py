from django.forms import SlugField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
# from store.models.store.product import Product



from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.Chapter import Chapter
from platform_web.models.app.project.Part import Part
from platform_web.models.app.project.ChapterPart import ChapterPart

def project_parts_view(request: HttpRequest, slug: str) -> HttpResponse:
	"""
	Shows all chapters and their ordered parts for a given project.
	"""
	project = get_object_or_404(Project, slug=slug)
	chapters = (
		Chapter.objects.filter(project=project)
		.prefetch_related('parts', 'chapter_parts__part')
		.order_by('order', 'title')
	)
	chapter_data = []
	for chapter in chapters:
		# Get parts in chapter, ordered by ChapterPart.order
		chapter_parts = (
			ChapterPart.objects.filter(chapter=chapter)
			.select_related('part')
			.order_by('order')
		)
		parts = [cp.part for cp in chapter_parts]
		chapter_data.append({
			'chapter': chapter,
			'parts': parts,
		})
	return render(request, "website/project/parts_view.html", {
		"project": project,
		"chapter_data": chapter_data,
	})
