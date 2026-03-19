import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from api.models import UserProfile


class TelegramStartAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("telegram_token", "").strip()
        
        if not token:
            return Response(
                {"error": "Please provide a telegram_token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate UUID4 token format
        try:
            uuid_token = uuid.UUID(token, version=4)
        except (ValueError, AttributeError):
            return Response(
                {"error": "Invalid token format."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Find user by token
        user_profile = (
            UserProfile.objects.filter(telegram_connection_token=uuid_token)
            .select_related("user")
            .first()
        )

        if not user_profile or not user_profile.user:
            return Response(
                {
                    "error": "User not found for this token. Did you provide the correct one?"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        user = user_profile.user

        # Optionally, generate JWT for bot
        jwt = AccessToken.for_user(user)

        user_data = {
            "id": user.pk,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "jwt": str(jwt),
        }

        return Response({"user": user_data}, status=status.HTTP_200_OK)
