from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import LoginSerializer, RefreshSerializer
from .application.login_use_case import LoginUseCase
from .application.refresh_use_case import RefreshUseCase

from authentication.domain.exceptions import InvalidCredentialsError, InactiveUserError


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = LoginUseCase().execute(**serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        except InvalidCredentialsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except InactiveUserError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)


class RefreshView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            data = RefreshUseCase().execute(
                refresh_token=serializer.validated_data["refresh"],
            )
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
