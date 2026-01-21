from django.urls import path
from platform_web.views import *


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/projects/", projects_view, name="projects"),
    path("dashboard/map/", MapView.as_view(), name="dashboard_map"),
    path("dashboard/levels/", LevelsView.as_view(), name="levels"),
    # path("contact/", ContactView.as_view(), name="contact"),
    
    # path("jobs/", JobsView.as_view(), name="jobs"),
    # path("job_single/<int:id>/", JobDetailView.as_view(), name="job_single"),
    # path("delete_job/<int:pk>/", JobDeleteView.as_view(), name="delete_job"),
    # path("edit_job/<int:pk>/", JobEditView.as_view(), name="edit_job"),
    # path("add_job/", JobCreateView.as_view(), name="add_job"),
    
    # path("login/", CustomLoginView.as_view(), name="login"),
    path("account/logout/", CustomLogoutView.as_view(), name="logout"),
    # path("signup/", SignupView.as_view(), name="signup"),
    
    
    # auth
    # path("account/profile/", ProfileView.as_view(), name="profile")
    
     # extra
    # path("search/", search_results, name="search_results"),
    # path("not-found-preview/", NotFoundPreview.as_view(), name="not_found_preview"),
]
