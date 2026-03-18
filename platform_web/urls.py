from django.urls import path
from platform_web.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # Auth
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Dashboard
    path("dashboard/projects/", projects_view, name="projects"),

    # Project
    path("project/<slug:slug>/", project_details_view, name="project_details"),
    path("project/<slug:slug>/lesson/<int:order>/", lesson_details_view, name="lesson_details"),
]
