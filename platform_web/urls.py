from django.urls import path
from platform_web.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # Account
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Dashboard
    path("dashboard/projects/", projects_view, name="projects"),
    path("dashboard/courses/", courses_view, name="courses"),
    path("dashboard/settings/", SettingsView.as_view(), name="settings"),
    
    # Project
    path("projects/<slug:slug>/", project_details_view, name="project_details"),
    path("projects/<slug:slug>/lesson/<int:order>/", lesson_details_view, name="lesson_details"),
    
]
