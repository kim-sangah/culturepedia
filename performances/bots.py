from django.conf import settings
from openai import OpenAI
import openai
from .models import Performance
from django.db.models import Q
from PIL import Image
import pytesseract
CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY,)

# 사용자가 리뷰하거나 찜한 공연과 입력받은 해시태그를 바탕으로 공연 추천
def generate_recommendations(user_preferences, input_tags):
    # user_preferences에 있는 공연들을 context로 줌
    context = f"User is interested in the following performances: {', '.join(user_preferences)}\n"

    # input_tags가 있을 경우, input_tags를 context에 추가
    if input_tags:
        context += f"These are the tags the user has selected: {', '.join(input_tags)}\n"

    # 공연중, 공연예정인 공연들을 performance_list로 줌
    performance_list = Performance.objects.filter(
        Q(state="공연중") | Q(state="공연예정"))

    # performance_list에 있는 각 공연들의 제목과 공연 종류, 줄거리, 해시태그를 context로 줌
    for performance in performance_list:
        context += f"Performance: {performance['title']},
        Type: {performance['type']},
        Synopsis: {performance['synopsis']},
        Hashtags: {performance['performance_hashtag']}\n"

    prompt = context + "Based on the performances in user_preferences and selected tags in input_tags, recommend performances for the user."
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
        temperature=0.7,  # 모델 응답의 '창의성' 조절
        n=1,  # 응답 개수
        stop=None  # max_token 제한 도달할 때까지 토큰 생성
    )

    return response.choices[0].text.strip()

# 데이터가 없는(리뷰를 작성하거나 찜한 공연이 없는) 사용자로부터 입력받은 해시태그로만 공연 추천
def generate_recommendations_with_tags(input_tags):
    context = f"These are the tags the user has selected: {', '.join(input_tags)}\n"

    # 공연중, 공연예정인 공연들을 performance_list로 줌
    performance_list = Performance.objects.filter(
        Q(state="공연중") | Q(state="공연예정"))

    # performance_list에 있는 각 공연들의 제목과 공연 종류, 줄거리, 해시태그를 context로 줌
    for performance in performance_list:
        context += f"Performance: {performance['title']},
        Type: {performance['type']},
        Synopsis: {performance['synopsis']},
        Hashtags: {performance['performance_hashtag']}\n"

    prompt = context + \
        "Based on the selected tags in input_tags, recommend performances for the user."
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
        temperature=0.7,  # 모델 응답의 '창의성' 조절
        n=1,  # 응답 개수
        stop=None  # max_token 제한 도달할 때까지 토큰 생성
    )

    return response.choices[0].text.strip()

# 줄거리 생성
def generate_synopsis(performance):
    # 줄거리가 없는 공연의 소개이미지나 포스터에 있는 글 추출해 줄거리(공연 설명) 생성
    if performance.styurls and not performance.synopsis: # 소개이미지가 있는 경우
        for styurl in performance.styurls:
            try:
                text = pytesseract.image_to_string(Image.open(styurl), lang='kor+eng', timeout=3)
                if text.strip(): # 추출된 텍스트가 비어있지 않은지 체크
                    styurls_text += text
                else:
                    return "소개이미지에서 텍스트를 추출할 수 없습니다."
            except RuntimeError as TimeoutError:
                print(f"Error occurred while processing image: {TimeoutError}")
                continue

        context = f"This is the text embedded in a descriptive image of a performance: {styurls_text}\n"
        prompt = context + \
            "Based on the text, generate a concise synopsis or a description of the performance."

        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=prompt,
            max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
            temperature=0.7,  # 모델 응답의 '창의성' 조절
            n=1,  # 응답 개수
            stop=None  # max_token 제한 도달할 때까지 토큰 생성
        )
        performance.synopsis = response.choices[0].text.strip()  # 생성된 synopsis를 string으로 저장
    elif performance.poster and not performance.synopsis: # 소개이미지는 없고 포스터는 있는 경우
        try:
            poster_text = pytesseract.image_to_string(Image.open(performance.poster), lang='kor+eng', timeout=3)
            if poster_text.strip():  # 추출된 텍스트가 비어있지 않은지 체크
                context = f"This is the text embedded in a performance's poster: {poster_text}\n"
                prompt = context + \
                "Based on the text, generate a concise synopsis or a description of the performance."

                response = openai.Completion.create(
                    engine="gpt-4o-mini",
                    prompt=prompt,
                    max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
                    temperature=0.7,  # 모델 응답의 '창의성' 조절
                    n=1,  # 응답 개수
                    stop=None  # max_token 제한 도달할 때까지 토큰 생성
                )
                performance.synopsis = response.choices[0].text.strip()  # 생성된 synopsis를 string으로 저장
            else:
                return "포스터에서 텍스트를 추출할 수 없습니다."
        except RuntimeError as TimeoutError:
            print(f"Error occurred while processing poster: {TimeoutError}")
    else: # 소개 이미지도 없고 포스터도 없는 경우
        return "줄거리를 생성할 수 없습니다."

# 해시태그 생성
def generate_hashtags_for_performance(performance):
    # 줄거리가 있고 해시태그가 생성되지 않은 공연
    if performance.synopsis and not performance.hashtags:
        context = f"This is the synopsis of a performance: {performance.synopsis}\n"
        prompt = context + \
            "Based on the synopsis, generate three hashtags that best describe the performance."

        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=prompt,
            max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
            temperature=0.7,  # 모델 응답의 '창의성' 조절
            n=1,  # 응답 개수
            stop=None  # max_token 제한 도달할 때까지 토큰 생성
        )
        hashtags = response.choices[0].text.strip().split()[:3]
        for tag in hashtags:
            performance.performance_hashtag = tag # 수정 필요
        performance.save()
        return performance.performance_hashtag.all()
    # 줄거리가 없고(소개이미지나 포스터도 없어서 줄거리 생성이 되지 않음) 해시태그가 생성되지 않은 공연
    elif not performance.synopsis and not performance.hashtags:
        # 공연의 필드 일부를 정보로 주고 이를 바탕으로 해시태그를 생성하게 함
        context = f"These are available informations of a performance:
        {performance.title},
        {performance.type},
        {performance.runtime},
        {performance.age},
        {performance.daehakro},
        {performance.festival},
        {performance.musicallicense},
        {performance.musicalcreate}"

        prompt = context + "Based on the available information, generate three hashtags that best describe the performance."

        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=prompt,
            max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
            temperature=0.7,  # 모델 응답의 '창의성' 조절
            n=1,  # 응답 개수
            stop=None  # max_token 제한 도달할 때까지 토큰 생성
        )
        hashtags = response.choices[0].text.strip().split()[:3]
        for tag in hashtags:
            performance.performance_hashtag = tag # 수정 필요
        performance.save()
        return performance.performance_hashtag.all()

# def recommendation_bot(user_input):
#     system_instructions = """
#     You are a helpful assistant.
#     """
#     completion = CLIENT.chat.completions.create(
#         model = "gpt-4o-mini",
#         messages = [
#             {
#                 "role": "system",
#                 "content": system_instructions,
#             },
#             {
#                 "role": "user",
#                 "content": user_input,
#             }
#         ],
#     )
#     return completion.choices[0].message.content
