from django.urls import path
from platform_web.views import *
from platform_web.views.single_views import project_parts_view, part_detail_view, project_details_view

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/projects/", projects_view, name="projects"),
    path("dashboard/map/", MapView.as_view(), name="dashboard_map"),
    # path("dashboard/levels/", LevelsView.as_view(), name="levels"),
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    # Project detail view (new inner project page)
    path("project/<slug:slug>/", project_details_view, name="project_details"),
    # Project parts view (old inner project view)
    path("project/<slug:slug>/parts/", project_parts_view, name="project_parts_view"),
    # path("project/<slug:slug>/part/<int:order>/", part_detail_view, name="part_detail"),
    path("project/<slug:slug>/part/<int:order>/", part_detail_view, name="part_detail"),
]
