from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from gym.models import User as GymUser


class RefreshUseCase:
    def execute(self, refresh_token: str) -> dict:
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            raise ValueError("Refresh token inválido ou expirado.")

        user_id = refresh.payload.get("user_id")
        try:
            user = GymUser.objects.get(pk=user_id)
        except GymUser.DoesNotExist:
            raise ValueError("Usuário não encontrado.")

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "username": user.full_name,
            "email": user.email,
            "level": user.level,
        }
