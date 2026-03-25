from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class GymJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that resolves the user from gym.User
    instead of django.contrib.auth.User, eliminating the auth_user dependency.
    """

    def get_user(self, validated_token):
        from gym.models import User as GymUser

        user_id = validated_token.get("user_id")
        if not user_id:
            raise InvalidToken("Token sem user_id.")

        try:
            user = GymUser.objects.get(pk=user_id, deleted_at__isnull=True)
        except GymUser.DoesNotExist:
            raise AuthenticationFailed("Usuário não encontrado.")

        if user.status != "active":
            raise AuthenticationFailed("Usuário inativo.")

        return user
