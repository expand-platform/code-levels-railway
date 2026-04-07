import uuid

from numpy import require
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from api.models.UserProfile import UserProfile


class TelegramAccessLevelView(APIView):
    permission_classes = [AllowAny]
    required_fields = ["telegram_user_id"]

    def get(self, request: Request):
        telegram_user_id = request.query_params.get("telegram_user_id")
        if not telegram_user_id:
            return Response(
                {"error": "telegram_user_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_profile = (
            UserProfile.objects.filter(telegram_user_id=telegram_user_id)
            .select_related("user")
            .first()
        )
        if not user_profile or not user_profile.user:
            return Response({"access_level": "visitor"}, status=status.HTTP_200_OK)
        
        user = user_profile.user
        if user.is_superuser:
            access_level = "super_admin"
        elif user.is_staff:
            access_level = "admin"
        else:
            access_level = "user"
        return Response({"access_level": access_level}, status=status.HTTP_200_OK)


class ValidateTelegramTokenView(APIView):
    permission_classes = [AllowAny]
    required_fields = ["user_input", "telegram_user_id", "telegram_first_name"]

    def post(self, request: Request):
        token = request.data.get("user_input", "").strip()

        if not token:
            return Response(
                {"error": "⚠️ Please provide a token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate UUID4 token format
        try:
            uuid_token = uuid.UUID(token, version=4)
        except (ValueError, AttributeError):
            return Response(
                {"error": "❌ Token format is invalid, sorry"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find user by token
        user_profile = (
            UserProfile.objects.filter(telegram_connection_token=uuid_token)
            .select_related("user")
            .first()
        )

        if not user_profile or not user_profile.user:
            return Response(
                {"error": "❌ Can't find the user. Did you provide the correct token?"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # if token already verified, return error
        if user_profile.is_token_verified:
            return Response(
                {"error": "🙉 This token has already been verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = user_profile.user

        # update user profile with telegram info
        telegram_user_id = request.data.get("telegram_user_id")
        telegram_first_name = request.data.get("telegram_first_name")
        if telegram_user_id and telegram_first_name:
            user_profile.update_telegram_info(telegram_user_id, telegram_first_name)
            print(
                f"🟢 Updated Telegram info for user {user.username}: {telegram_user_id}, {telegram_first_name}"
            )

        # Optionally, generate JWT for bot
        jwt = AccessToken.for_user(user)

        print(
            f"🟢 User {user.username} authenticated with Telegram! ID: {telegram_user_id}, first_name: {telegram_first_name}. Generated JWT token for 5 minutes: {jwt}"
        )

        user_data = {
            "id": user.pk,
            "username": user.username,
            "first_name": telegram_first_name,
            "jwt": str(jwt),
        }

        return Response(user_data, status=status.HTTP_200_OK)
