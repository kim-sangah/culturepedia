from .models import User
from django.core.validators  import validate_email
from django.core.exceptions  import ValidationError
import re

def validate_user_data(user_data):
    email = user_data.get("email")
    password = user_data.get("password")
    username = user_data.get("username")
    gender = user_data.get("gender")
    birthday = user_data.get("birthday")

    # email 형식 검증 
    try:
        validate_email(email)
    except ValidationError:
        return "유효하지않는 이메일형식입니다."
    
    # email 중복 여부 확인
    if User.objects.filter(email=email).exists():
        return "이미 다른 사용자가 이메일을 사용하고 있습니다."
    
    # username 중복 여부 확인
    if User.objects.filter(username=username).exists():
        return "이미 다른 사용자가 이름을 사용하고 있습니다."
    
    # password 최소 길이 검증
    if len(password) < 8:
        return "비밀번호는 최소 8자리여야 합니다."
    
    # # gender 입력 검증 ##필수입력이 되어 임시 주석 처리
    # if gender not in ['M', 'F']: # M,F, 남,여 만 허용
    #     return "성별은 'M' 또는 'F'만 입력할 수 있습니다."
    
    # birthday 형식 검증
    if birthday:
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_pattern.match(birthday):
            return "생년월일은 YYYY-MM-DD 형식으로 입력해야 합니다."

    return None