from .Home import HomeView
from .Dashboard import DashboardView
from .Settings import SettingsView
from .Changelog import WebsiteChangelogView
from .Projects import (
	projects_view,
	courses_view,
	project_details_view,
	lesson_details_view,
)
from .auth.logout import CustomLogoutView, LogoutView, logout_then_login
from .functional.robots import robots_txt
from .NotFound import NotFoundPreview, NotFoundView, not_found_404

__all__ = [
	"HomeView",
	"DashboardView",
	"SettingsView",
	"WebsiteChangelogView",
	"projects_view",
	"courses_view",
	"project_details_view",
	"lesson_details_view",
	"CustomLogoutView",
	"LogoutView",
	"logout_then_login",
	"robots_txt",
	"NotFoundPreview",
	"NotFoundView",
	"not_found_404",
]
