from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserModifySerializer
from .validators import validate_user_data
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken


#회원가입
class UserSignupView(APIView):
    def post(self, request):
        
        errors = validate_user_data(request.data)
        
        if errors is not None:
            return Response({"message": errors}, status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.create_user(
            email = request.data.get("email"),
            password = request.data.get("password"),
            username = request.data.get("username"),
            gender = request.data.get("gender"),
            birthday= request.data.get("birthday"),
        )

        refresh = RefreshToken.for_user(user)
        response_dict = {"message": "회원가입이 완료되었습니다."}
        response_dict['access'] = str(refresh.access_token)
        response_dict['refresh'] = str(refresh)
        return Response(response_dict)


#로그인
class UserSigninView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        #이메일 또는 비밀번호가 비어 있는지 확인
        if not email or not password:
            return Response({"message": "이메일과 비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        #이메일과 비밀번호로 사용자 인증
        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "username": (user.username),
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "이메일 또는 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


#로그아웃
class UserSignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"message": "비밀번호가 틀렸습니다."},status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_205_RESET_CONTENT)


#프로필
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    #프로필 조회
    def get(self, request, pk):
        #print(f"Requested user ID : {pk}")
        user = get_object_or_404(User, id=pk)
        

        if request.user != user:
            raise PermissionDenied(status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = UserSerializer(user)
        #print(f"데이터 입력 : {serializer.data}")
        return Response(serializer.data)
    
    #회원정보 수정
    def put(self, request, pk):
        user = get_object_or_404(User, id=pk)
        if request.user != user:
            raise PermissionDenied(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserModifySerializer(user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            password = request.data.pop('password', None)
            if password is not None: 
                serializer.save()
                user.set_password(password)
                user.save()
            else:
                serializer.save()
            return Response({"message": "회원정보수정이 완료되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#회원탈퇴
class UserDeleteView(APIView):
    def delete(self,request,pk=None):
        user = request.user
        password = request.data.get("password")
        
        if not password:
            return Response({"message": "비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"message": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = False
        user.save()

        return Response({"message": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)