from django.views.generic import TemplateView


class NotFoundPreview(TemplateView):
    template_name = "website/pages/404.html"


class NotFoundView(TemplateView):
    template_name = "website/pages/404.html"


def not_found_404(request, exception):
    not_found_404_view = NotFoundView.as_view()
    return not_found_404_view(request, exception=exception)
