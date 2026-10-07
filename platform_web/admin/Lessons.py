from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_summernote.widgets import SummernoteWidget
from django import forms

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin

from platform_web.admin.Skills import SkillContentsWidget
from platform_web.models.project.Lesson import Lesson
from platform_web.models.project.Project import Project


class LessonInlineForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("order", "title", "objectives")
        labels = {
            "order": _("ID"),
        }
        widgets = {
            "objectives": SkillContentsWidget.compact(),
        }


class LessonsInline(SortableInlineAdminMixin, admin.TabularInline):  # type: ignore[misc]
    model = Lesson
    form = LessonInlineForm
    extra = 1
    fields = ("order", "title", "objectives")
    ordering = ["order"]
    show_change_link = True


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
        widgets = {
            "description": SummernoteWidget(),
            "objectives": SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Only for new Lesson
            latest_project = Project.objects.order_by("-id").first()
            if latest_project:
                self.fields["project"].initial = latest_project


@admin.register(Lesson)
class LessonsAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    form = LessonAdminForm
    changeform_format = "horizontal_tabs"
    list_display = ("order", "title", "type", "project", "last_edited")
    search_fields = ("title", "project__title")
    list_filter = ("project",)
    ordering = ("order",)
    readonly_fields = ("last_edited", "uuid")
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "project",
                    "title",
                    "type",
                    "thumbnail",
                    "youtube_url",
                    "codepen_url",
                    "description",
                    "objectives",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "order",
                    "slug",
                    "uuid",
                    "last_edited",
                )
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("order")
