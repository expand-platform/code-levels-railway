from django.urls import path
from platform_web.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # Account
    path("settings/", SettingsView.as_view(), name="settings"),
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Projects, topics, courses
    path("projects/", projects_view, name="projects"),
    path("topics/", topics_view, name="topics"),
    path("courses/", courses_view, name="courses"),
    
    # sort by project / language
    path(
        "projects/course/<slug:course_slug>/",
        projects_by_course_view,
        name="projects_by_course",
    ),
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
    path("projects/<slug:slug>/lesson/<int:order>/", lesson_details_view, name="lesson_details"),
]
