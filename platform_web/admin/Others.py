from django.contrib import admin
from django_summernote.widgets import SummernoteWidget
from django import forms

from adminsortable2.admin import SortableAdminMixin

from platform_web.models.blog.BlogPost import BlogPost
from platform_web.models.project.Difficulty import Difficulty
from platform_web.models.project.Framework import Framework
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.user.PaidPlan import PaidPlan


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class StagesAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


@admin.register(Difficulty)
class DifficultiesAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("order", "name")


@admin.register(PaidPlan)
class PaidPlansAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("ui_order", "title", "name", "access_level", "price")


@admin.register(Framework)
class FrameworkAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("order", "name")
    search_fields = ("name",)


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"
        widgets = {
            "content": SummernoteWidget(),
        }


@admin.register(BlogPost)
class BlogPostsAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ("title", "is_published", "is_featured", "published_at", "updated_at")
    list_filter = ("is_published", "is_featured", "created_at", "published_at")
    search_fields = ("title", "content", "excerpt")
    readonly_fields = ("uuid", "created_at", "updated_at", "excerpt")
    ordering = ("-published_at",)
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "title",
                    "featured_image",
                    "content",
                    "is_published",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "excerpt",
                    "seo_title",
                    "seo_description",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "is_featured",
                    "published_at",
                )
            },
        ),
        (
            "Meta",
            {
                "fields": (
                    "slug",
                    "uuid",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
