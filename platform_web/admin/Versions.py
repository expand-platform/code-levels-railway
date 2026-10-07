from django.contrib import admin

from platform_web.models.base import Changelog


@admin.register(Changelog)
class WebsiteVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "title", "released_at")
    search_fields = ("version", "title")
    readonly_fields = ("released_at",)
