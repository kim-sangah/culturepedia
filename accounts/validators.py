from .models import User
from django.core.validators  import validate_email
from django.core.exceptions  import ValidationError

def validate_user_data(user_data):
    username = user_data.get("username")
    password = user_data.get("password")
    email = user_data.get("email")
    gender = user_data.get("gender")
    birthday = user_data.get("birthday")
    
    #email 형식 검증 
    try:
        validate_email(email)
    except ValidationError:
        return "유효하지않는 이메일형식입니다."
    
    #email 중복 여부 확인
    if User.objects.filter(email=email).exists():
        return "이미 다른 사용자가 이메일을 사용하고 있습니다."
    
    #username 중복 여부 확인
    if User.objects.filter(username=username).exists():
        return "이미 다른 사용자가 이름을 사용하고 있습니다."
    
    #password 최소 길이 검증
    if len(password) < 8:
        return "비밀번호는 최소 8자리여야 합니다."