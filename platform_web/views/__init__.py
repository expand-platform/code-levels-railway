from .pages.Home import HomeView
from .dashboard.Dashboard import DashboardChatView, DashboardPaymentView, DashboardView
from .pages.Settings import SettingsView
from .pages.Changelog import WebsiteChangelogView
from .projects.Roadmap import RoadmapView
from .projects.Jobs import JobsView
from .projects.Roadmaps import RoadmapsView
from .projects.Courses import CoursesView
from .projects.Projects import (
	projects_page_view,
	projects_view,
	projects_by_course_view,
	topics_view,
	concepts_view,
	topics_by_language_view,
	courses_view,
	courses_by_course_view,
	project_details_view,
	lesson_details_view,
)
from .auth.logout import CustomLogoutView, LogoutView, logout_then_login
from .seo.robots import robots_txt
from .pages.NotFound import NotFoundPreview, NotFoundView, not_found_404
from .pages.BlogView import BlogView, BlogDetailView


__all__ = [
	"HomeView",
	"DashboardView",
	"DashboardPaymentView",
	"DashboardChatView",
	"CoursesView",
	"SettingsView",
	"WebsiteChangelogView",
	"RoadmapView",
	"JobsView",
	"RoadmapsView",
	"projects_page_view",
	"projects_view",
	"projects_by_course_view",
	"topics_view",
	"concepts_view",
	"topics_by_language_view",
	"courses_view",
	"courses_by_course_view",
	"project_details_view",
	"lesson_details_view",
	"CustomLogoutView",
	"LogoutView",
	"logout_then_login",
	"robots_txt",
	"NotFoundPreview",
	"NotFoundView",
	"not_found_404",
	"BlogView",
	"BlogDetailView",
]
