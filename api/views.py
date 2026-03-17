from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.Lesson import Lesson
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Course import Course


class ReorderLessonsView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, project_slug):
        order_data = request.data.get("order", [])
        try:
            project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            return Response(
                {"success": False, "error": "Project not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Bulk update
        for item in order_data:
            lesson_id = item.get("id")
            lesson_order = item.get("order")
            Lesson.objects.filter(id=lesson_id, project=project).update(
                order=lesson_order
            )

        return Response({"success": True})


class ReorderProjectsByLanguageView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, language_id):
        order_data = request.data.get("order", [])
        try:
            language = ProgrammingLanguage.objects.get(id=language_id)
        except ProgrammingLanguage.DoesNotExist:
            return Response(
                {"success": False, "error": "Language not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        for item in order_data:
            project_id = item.get("id")
            project_order = item.get("order")
            Project.objects.filter(id=project_id, programming_languages=language).update(
                language_order=project_order
            )

        return Response({"success": True})


class ReorderProjectsByCourseView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, course_id):
        order_data = request.data.get("order", [])
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"success": False, "error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        for item in order_data:
            project_id = item.get("id")
            project_order = item.get("order")
            Project.objects.filter(id=project_id, course=course).update(
                course_order=project_order
            )

        return Response({"success": True})
