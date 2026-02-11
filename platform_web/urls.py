from django.urls import path
from platform_web.views import *
from platform_web.views.single_views import project_parts_view, lesson_details_view, project_details_view

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # Auth
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Dashboard
    path("dashboard/projects/", projects_view, name="projects"),

    # Project
    path("project/<slug:slug>/", project_details_view, name="project_details"),
    path("project/<slug:slug>/lesson/<int:order>/", lesson_details_view, name="lesson_details"),
    
    # API
    path("api/project/<slug:slug>/reorder_lessons/", reorder_lessons_view, name="reorder_lessons"),
    path("api/language/<int:language_id>/reorder_projects/", reorder_projects_by_language_view, name="reorder_projects_by_language"),
    path("api/course/<int:course_id>/reorder_projects/", reorder_projects_by_course_view, name="reorder_projects_by_course"),
]
