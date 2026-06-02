from django.urls import path
from platform_web.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # Account
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Main app routes
    path("projects/", projects_view, name="projects"),
    path(
        "projects/course/<int:course_id>/",
        projects_by_course_view,
        name="projects_by_course",
    ),
    path("topics/", topics_view, name="topics"),
    path(
        "topics/language/<int:language_id>/",
        topics_by_language_view,
        name="topics_by_language",
    ),
    path("courses/", courses_view, name="courses"),
    path(
        "courses/course/<int:course_id>/",
        courses_by_course_view,
        name="courses_by_course",
    ),
    path("settings/", SettingsView.as_view(), name="settings"),

    # Project
    path("projects/<slug:slug>/", project_details_view, name="project_details"),
    path("projects/<slug:slug>/lesson/<int:order>/", lesson_details_view, name="lesson_details"),
    
]
