from django.contrib.auth import authenticate
from authentication.domain.user import UserEntity


class DjangoUserRepository:
    def get_by_credentials(self, username: str, password: str) -> UserEntity | None:
        user = authenticate(username=username, password=password)
        if user is None:
            return None
        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )