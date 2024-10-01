from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 'username' 대신 'email'로 인증
        email = kwargs.get('email')
        if email is None or password is None: #이메일 또는 비밀번호가 없으면 None반환
            return None
        
        try:
            user = UserModel.objects.get(email=email) #이메일로 사용자 조회
        except UserModel.DoesNotExist: #이메일에 해당하는 사용자가 없으면 None 반환
            return None
        
        
        #  비밀번호 확인 및 사용자 인증 여부 확인
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        #사용자가 활성 상태인지 확인
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
