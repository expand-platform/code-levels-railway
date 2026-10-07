from django.shortcuts import redirect
from django.urls import path
from django.views.generic import RedirectView

from platform_web.middleware import require_courses, require_user_dashboard
from platform_web.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    # download
    path(
        "desktop-app/",
        lambda request: redirect("https://github.com/Ca-tt/codelevels-app/releases"),
        name="desktop_app",
    ),
    
    # Account
    path("settings/", require_user_dashboard(SettingsView.as_view()), name="settings"),
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),

    # Dashboard
    path("dashboard/", require_user_dashboard(DashboardView.as_view()), name="dashboard"),
    path("dashboard/payment/", require_user_dashboard(DashboardPaymentView.as_view()), name="dashboard_payment"),
    path("dashboard/chat/", require_user_dashboard(DashboardChatView.as_view()), name="dashboard_chat"),
    
    path("job-tracks/", JobsView.as_view(), name="job_tracks"),
    path(
        "job-tracks/course/<slug:course_slug>/",
        JobsView.as_view(),
        name="job_tracks_by_course",
    ),
    path(
        "roadmap/",
        RedirectView.as_view(pattern_name="job_tracks", permanent=True, query_string=True),
    ),
    path(
        "roadmap/course/<slug:course_slug>/",
        RedirectView.as_view(
            pattern_name="job_tracks_by_course", permanent=True, query_string=True
        ),
    ),
    path("roadmaps/", RoadmapsView.as_view(), name="roadmaps"),
    path(
        "roadmaps/course/<slug:course_slug>/",
        RoadmapsView.as_view(),
        name="roadmaps_by_course",
    ),
    path(
        "languages/",
        RedirectView.as_view(pattern_name="roadmaps", permanent=True, query_string=True),
    ),
    path(
        "languages/course/<slug:course_slug>/",
        RedirectView.as_view(
            pattern_name="roadmaps_by_course", permanent=True, query_string=True
        ),
    ),

    # Projects: course → skill → projects; ?view=default is the project grid
    path("projects/", projects_page_view, name="projects"),
    path(
        "projects/course/<slug:course_slug>/",
        projects_page_view,
        name="projects_by_course",
    ),

    # Topics, courses
    path("topics/", topics_view, name="topics"),
    path("concepts/", concepts_view, name="concepts"),
    path("courses/", require_courses(CoursesView.as_view()), name="courses"),
    
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
