from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.domain.exceptions import InvalidCredentialsError, InactiveUserError
from gym.models import User as GymUser


class LoginUseCase:
    def execute(self, email: str, password: str) -> dict:
        try:
            user = GymUser.objects.get(email=email)
        except GymUser.DoesNotExist:
            raise InvalidCredentialsError("Credenciais inválidas.")

        if not check_password(password, user.password):
            raise InvalidCredentialsError("Credenciais inválidas.")

        if user.status == "inactive":
            raise InactiveUserError("Usuário inativo.")

        # Gera token JWT com claims customizados sem depender de auth.User
        refresh = RefreshToken()
        refresh["user_id"] = user.id
        refresh["email"] = user.email
        refresh["level"] = user.level

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "username": user.full_name,
            "email": user.email,
            "level": user.level,
        }
