from django.http import HttpRequest, JsonResponse

from platform_web.services.model.SearchService import SearchService


def project_search_index_view(request: HttpRequest) -> JsonResponse:
    response = JsonResponse({"projects": SearchService.catalog()})
    response["Cache-Control"] = "no-store"
    return response
