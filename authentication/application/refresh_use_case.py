from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class RefreshUseCase:
    def execute(self, refresh_token: str) -> dict:
        try:
            refresh = RefreshToken(refresh_token)
            return {
                "access": str(refresh.access_token),
            }
        except TokenError:
            raise ValueError("Refresh token inválido ou expirado.")