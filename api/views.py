from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from platform_web.models.project.Project import Project
from platform_web.models.project.Lesson import Lesson
from platform_web.models.project.Course import Course
from platform_web.models.project.Skill import Skill


def _apply_order(model, order_data, order_field, **filters):
    for item in order_data:
        obj_id = item.get("id")
        obj_order = item.get("order")
        if obj_id is None or obj_order is None:
            continue
        model.objects.filter(id=obj_id, **filters).update(**{order_field: obj_order})


def _get_or_error(model, error_msg, **lookup):
    try:
        return model.objects.get(**lookup), None
    except model.DoesNotExist:
        return None, Response(
            {"success": False, "error": error_msg},
            status=status.HTTP_404_NOT_FOUND,
        )


class ReorderLessonsView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, project_slug):
        project, error = _get_or_error(Project, "Project not found.", slug=project_slug)
        if error:
            return error
        _apply_order(Lesson, request.data.get("order", []), "order", project=project)
        return Response({"success": True})


class ReorderProjectsByCourseView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, course_id):
        course, error = _get_or_error(Course, "Course not found.", id=course_id)
        if error:
            return error
        _apply_order(
            Project, request.data.get("order", []), "course_order", course=course
        )
        return Response({"success": True})


class ReorderProjectsBySkillView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, skill_id):
        skill, error = _get_or_error(Skill, "Skill not found.", id=skill_id)
        if error:
            return error
        _apply_order(
            Project, request.data.get("order", []), "skill_order", skills=skill
        )
        return Response({"success": True})
