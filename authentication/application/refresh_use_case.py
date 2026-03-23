from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User as DjangoUser
from gym.models import User as GymUser


class RefreshUseCase:
    def execute(self, refresh_token: str) -> dict:
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            raise ValueError("Refresh token inválido ou expirado.")

        django_user_id = refresh.payload.get("user_id")
        try:
            django_user = DjangoUser.objects.get(id=django_user_id)
            gym_user = GymUser.objects.get(email=django_user.username)
        except (DjangoUser.DoesNotExist, GymUser.DoesNotExist):
            raise ValueError("Usuário não encontrado.")

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": gym_user.id,
            "username": gym_user.full_name,
            "email": gym_user.email,
            "level": gym_user.level,
        }
