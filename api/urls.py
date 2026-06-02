from django.urls import path
from api.views import (
    ReorderLessonsView,
    ReorderProjectsByCourseView,
)
from api.telegram_api import ValidateTelegramTokenView, TelegramAccessLevelView


urlpatterns = [
    path(
        "project/<slug:project_slug>/reorder_lessons/",
        ReorderLessonsView.as_view(),
        name="reorder-lessons",
    ),
    path(
        "course/<int:course_id>/reorder_projects/",
        ReorderProjectsByCourseView.as_view(),
        name="reorder-projects-by-course",
    ),
    path("telegram/validate-token/", ValidateTelegramTokenView.as_view(), name="telegram-validate-token"),
    path("telegram/access-level/", TelegramAccessLevelView.as_view(), name="telegram-access-level"),
]
