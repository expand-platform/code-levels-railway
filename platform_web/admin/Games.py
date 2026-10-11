from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from platform_web.models.project.Game import Game


@admin.register(Game)
class GameAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("order", "title", "link", "updated_at")
    search_fields = ("title", "description", "link")
    ordering = ("order", "title")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "title",
                    "image",
                    "description",
                    "link",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "order",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
