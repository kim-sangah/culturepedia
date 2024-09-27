from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.state import token_backend

# Create your views here.


class UserSigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = IsAuthenticated(email=email, password=password)
        if not user:
            return Response(
                {"message": "email과 Password가 일치하지 않거나 존재하지 않습니다."},
                status=400,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )


class UserSignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 사용자로부터 받은 토큰을 무효화합니다.
            refresh_token = request.data.get('refresh')
            print(refresh_token, request.data)
            if not refresh_token:
                return Response(
                    {'detail': 'Refresh token is required.'},
                    status=400
                )

            # RefreshToken 인스턴스를 생성하여 Blacklist에 추가합니다.
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'detail': 'Logged out successfully.'},
                status=200
            )

        except TokenError:
            return Response(
                {'detail': 'Token is invalid or expired.'},
                status=400
            )
