from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_summernote.widgets import SummernoteWidget
from django import forms

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from platform_web.config.web_config import WebsiteConfigScheme
from platform_web.models.blog.BlogPost import BlogPost

from platform_web.models.project.Course import Course
from platform_web.models.project.Project import Project
from platform_web.models.project.Lesson import Lesson
from platform_web.models.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.project.Difficulty import Difficulty
from platform_web.models.project.Framework import Framework
from platform_web.models.project.Skill import Skill

from platform_web.models.base import WebsiteConfig
from platform_web.models.base import SocialMediaLink
from platform_web.models.base import Changelog

from platform_web.models.user.PaidPlan import PaidPlan


# inlines
class InlineSocialMediaLink(admin.TabularInline):
    model = SocialMediaLink
    extra = 1


class WebsiteConfigAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WebsiteConfig._meta.fields]
    list_display_links = (WebsiteConfigScheme.id, WebsiteConfigScheme.site_name)
    inlines = [InlineSocialMediaLink]

    # Only allow add if no config exists
    def has_add_permission(self, request: HttpRequest):
        return not WebsiteConfig.objects.exists()


admin.site.register(WebsiteConfig, WebsiteConfigAdmin)
admin.site.register(SocialMediaLink)


@admin.register(Changelog)
class WebsiteVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "title", "released_at")
    search_fields = ("version", "title")
    readonly_fields = ("released_at",)


class SkillsInline(SortableInlineAdminMixin, admin.TabularInline):  # type: ignore[misc]
    model = Skill
    extra = 1
    fields = ("name", "order")
    ordering = ["order"]
    show_change_link = True


class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("order", "title")
    search_fields = ("title",)
    inlines = [SkillsInline]


class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class StagesAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


class LessonsInline(SortableInlineAdminMixin, NestedTabularInline):
    model = Lesson
    extra = 1
    fields = ("title", "order", "description")
    ordering = ["order"]


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "description": SummernoteWidget(),
            "stages": SummernoteWidget(),
        }


class ProjectAdmin(SortableAdminMixin, NestedModelAdmin):  # type: ignore[misc]
    form = ProjectAdminForm
    inlines = [LessonsInline]
    changeform_format = "horizontal_tabs"
    list_display = (
        "course_order",
        "title",
        "course",
        "type",
        "get_programming_languages",
        "updated_at",
    )
    list_filter = ("type", "course")
    search_fields = ("title", "description")
    ordering = ("course_order",)
    readonly_fields = ("uuid", "created_at", "updated_at")
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "title",
                    "image",
                    "type",
                    "course",
                    "programming_languages",
                    "difficulty",
                    "framework",
                    "codepen_url",
                    "description",
                    "stages",
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
                    "is_active",
                    "is_video_course",
                    "language_order",
                    "course_order",
                    "skill_order",
                    "order",
                    "slug",
                    "uuid",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    actions = ["publish_projects", "unpublish_projects"]

    def publish_projects(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} project(s) published.")

    publish_projects.short_description = "Publish selected projects"  # type: ignore[attr-defined]

    def unpublish_projects(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} project(s) unpublished.")

    unpublish_projects.short_description = "Unpublish selected projects"  # type: ignore[attr-defined]

    def get_programming_languages(self, obj):
        return ", ".join([pl.name for pl in obj.programming_languages.all()])

    def get_framework(self, obj):
        return ", ".join([fw.name for fw in obj.framework.all()])

    get_programming_languages.short_description = "Languages"  # type: ignore[attr-defined]
    get_framework.short_description = "Frameworks"  # type: ignore[attr-defined]


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


class SkillAdminForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        projects_field = self.fields.get("projects")
        if not projects_field:
            return
        if self.instance.pk and self.instance.related_course_id:
            projects_field.queryset = Project.objects.filter(
                course_id=self.instance.related_course_id,
                is_active=True,
            ).order_by("skill_order", "course_order", "title")
        else:
            projects_field.queryset = Project.objects.filter(is_active=True)
            projects_field.help_text = _(
                "Save the skill with a course first, then assign projects from that course."
            )


class SkillsAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    form = SkillAdminForm
    list_display = ("order", "name", "related_course")
    list_filter = ("related_course",)
    search_fields = ("name",)
    ordering = ("order",)
    filter_horizontal = ("projects",)
    readonly_fields = ("uuid",)
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "name",
                    "related_course",
                    "projects",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "order",
                    "uuid",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("related_course")


class DifficultiesAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("order", "name")


class PaidPlansAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ("ui_order", "title", "name", "access_level", "price")


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


admin.site.register(Course, CourseAdmin)
admin.site.register(Skill, SkillsAdmin)
admin.site.register(Difficulty, DifficultiesAdmin)

admin.site.register(ProgrammingLanguage, ProgrammingLanguageAdmin)
admin.site.register(Framework, FrameworkAdmin)
admin.site.register(BlogPost, BlogPostsAdmin)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Lesson, LessonsAdmin)

admin.site.register(PaidPlan, PaidPlansAdmin)
