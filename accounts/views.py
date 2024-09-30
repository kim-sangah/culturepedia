from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated #인증된 사용자만 접근가능하도록 하기
from .models import User
from .serializers import UserSerializer
from .validators import validate_user_data
from rest_framework_simplejwt.tokens import RefreshToken


#회원가입
class UserSignupView(APIView):
    def post(self, request):
        
        errors = validate_user_data(request.data) #에러일 시 에러 메시지 반환
        
        if errors is not None:
            return Response({"message": errors}, status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.create_user(
            username = request.data.get("username"),
            password = request.data.get("password"),
            email = request.data.get("email"),
            gender = request.data.get("gender"),
            birthday= request.data.get("birthday"),
        )
        
        # user = User.objects.create_user(**request.data)

        refresh = RefreshToken.for_user(user) #토근발급
        serializers = UserSerializer(user)
        response_dict = serializers.data
        response_dict['access'] = str(refresh.access_token)
        response_dict['refresh'] = str(refresh)
        return Response(response_dict)


#로그인
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 이메일 또는 비밀번호가 비어 있는지 확인
        if not email or not password:
            return Response({"error": "이메일과 비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 이메일과 비밀번호로 사용자 인증
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # 로그인 성공 시 토큰 발급
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': "로그인 성공",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "이메일 또는 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


#로그아웃
class UserSignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message":"로그아웃 되었습니다"}, status=status.HTTP_205_RESET_CONTENT)


#회원탈퇴
class UserSignupDelete(APIView):
    permission_classes = [IsAuthenticated] 
    
    def delete(self, request):
        user = request.user
        password = request.data.get("password")
        
        if not password:
            return Response({"error": "비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 확인
        if not user.check_password(password):
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호가 일치하면 사용자 삭제
        user.delete()
        return Response({"message": "사용자가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


#프로필 조회
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        if request.user != user:
            raise PermissionDenied(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)


#프로필 수정
class UserModifyView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        if request.user != user:
            raise PermissionDenied(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)