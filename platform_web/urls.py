from django.urls import path
from platform_web.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # Auth
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Dashboard
    path("dashboard/projects/", projects_view, name="projects"),
    path("dashboard/projects/<str:lang>/", projects_view, name="projects_by_lang"),
    path("dashboard/settings/", SettingsView.as_view(), name="settings"),
    path("set-language/", set_language_and_save, name="set_language_and_save"),

    # Project
    path("<str:lang>/projects/<slug:slug>/", project_details_view, name="project_details"),
    path("<str:lang>/projects/<slug:slug>/lesson/<int:order>/", lesson_details_view, name="lesson_details"),
]
