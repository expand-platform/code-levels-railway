from django.urls import path
from api.views import (
    ReorderLessonsView,
    ReorderProjectsByLanguageView,
    ReorderProjectsByCourseView,
)
from api.telegram_api import TelegramStartAPIView


urlpatterns = [
    path(
        "project/<slug:project_slug>/reorder_lessons/",
        ReorderLessonsView.as_view(),
        name="reorder-lessons",
    ),
    path(
        "language/<int:language_id>/reorder_projects/",
        ReorderProjectsByLanguageView.as_view(),
        name="reorder-projects-by-language",
    ),
    path(
        "course/<int:course_id>/reorder_projects/",
        ReorderProjectsByCourseView.as_view(),
        name="reorder-projects-by-course",
    ),
    path("telegram/connect/", TelegramStartAPIView.as_view(), name="telegram-connect"),
]
