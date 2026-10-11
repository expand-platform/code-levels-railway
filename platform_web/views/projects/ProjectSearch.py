from django.http import HttpRequest, JsonResponse

from platform_web.services.model.ProjectSearchService import ProjectSearchService


def project_search_index_view(request: HttpRequest) -> JsonResponse:
    response = JsonResponse({"projects": ProjectSearchService.catalog()})
    response["Cache-Control"] = "no-store"
    return response
