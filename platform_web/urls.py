from django.urls import path
from platform_web.views import *
from django.shortcuts import redirect

from platform_web.views import BlogView, BlogDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # download
    path(
        "desktop-app/",
        lambda request: redirect("https://github.com/Ca-tt/codelevels-app/releases"),
        name="desktop_app",
    ),
    
    # Account
    path("settings/", SettingsView.as_view(), name="settings"),
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    
    path("roadmap/", JobsView.as_view(), name="roadmap"),
    path(
        "roadmap/course/<slug:course_slug>/",
        JobsView.as_view(),
        name="roadmap_by_course",
    ),
    path("languages/", LanguagesView.as_view(), name="languages"),
    path(
        "languages/course/<slug:course_slug>/",
        LanguagesView.as_view(),
        name="languages_by_course",
    ),

    # Projects: course → projects; ?view=roadmap is course → skill → projects
    path("projects/", projects_page_view, name="projects"),
    path(
        "projects/course/<slug:course_slug>/",
        projects_page_view,
        name="projects_by_course",
    ),

    # Topics, courses
    path("topics/", topics_view, name="topics"),
    path("concepts/", concepts_view, name="concepts"),
    
    # sort by language
    path(
        "topics/language/<slug:language_slug>/",
        topics_by_language_view,
        name="topics_by_language",
    ),
    
    path(
        "courses/course/<int:course_id>/",
        courses_by_course_view,
        name="courses_by_course",
    ),
    
    # Project views
    path("projects/<slug:slug>/", project_details_view, name="project_details"),
    path("projects/<slug:slug>/<slug:part_slug>/", lesson_details_view, name="lesson_details"),

    # Blog
    path("blog/", BlogView.as_view(), name="blog"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog_details"),
]
