from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from platform_web.models.base import Changelog
from django.shortcuts import render


class WebsiteChangelogView(LoginRequiredMixin, View):
    template_name = "website/dashboard/pages/changelog.html"

    def get(self, request):
        versions = Changelog.objects.all()
        return render(request, self.template_name, {"versions": versions})
