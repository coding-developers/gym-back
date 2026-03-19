# application/login_use_case.py
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.domain.user import UserEntity
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

        user_entity = UserEntity(
            id=user.id,
            username=user.full_name,
            email=user.email,
            is_active=user.status == "active",
        )

        # SimpleJWT precisa de um objeto compatível com auth.User
        # Busca ou cria um auth.User espelho para gerar o token
        from django.contrib.auth.models import User as DjangoUser
        django_user, _ = DjangoUser.objects.get_or_create(
            username=user.email,
            defaults={"email": user.email}
        )

        refresh = RefreshToken.for_user(django_user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user_entity.id,
            "username": user_entity.username,
            "email": user_entity.email,
            "level": user.level,
        }