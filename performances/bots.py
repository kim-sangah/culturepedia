from django.conf import settings
from openai import OpenAI
import openai
from .models import Performance
from django.db.models import Q
CLIENT = OpenAI(api_key = settings.OPENAI_API_KEY,)

def generate_recommendation(user_preferences):
    # user_preferences에 있는 공연들을 context로 줌
    context = f"User is interested in the following performances: {', '.join(map(str, user_preferences))}\n"

    # 공연중, 공연예정인 공연들을 performance_list로 줌
    performance_list = Performance.objects.filter(Q(state="공연중") | Q(state="공연예정"))

    # performance_list에 있는 각 공연들의 제목과 공연 종류를 context로 줌
    for performance in performance_list:
        context += f"Performance: {performance['title']}, Type: {performance['type']}\n"
    
    prompt = context + "Based on these preferences, recommend ongoing performances for the user."
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150, # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
        temperature=0.7, # 모델 응답의 '창의성' 조절
        n=1, # 응답 개수
        stop=None # max_token 제한 도달할 때까지 토큰 생성
    )
    
    return response.choices[0].text.strip()


def generate_synopsis(performances):
    pass


def generate_hashtags_for_performance(performance):
    # 줄거리가 있고 해시태그가 생성되지 않은 공연
    if performance.synopsis and not performance.hashtags:
        context = f"This is the synopsis of a performance: {performance.synopsis}\n"
        prompt = context + "Based on the synopsis, generate three hashtags that best describe the performance."

        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=prompt,
            max_tokens=150, # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
            temperature=0.7, # 모델 응답의 '창의성' 조절
            n=1, # 응답 개수
            stop=None # max_token 제한 도달할 때까지 토큰 생성
        )
        hashtags = response.choices[0].text.strip().split()[:3]
        performance.hashtags = " ".join(hashtags)  # 생성된 해시태그들을 string으로 저장
        performance.save()
        return performance.hashtags
    # 줄거리가 없고 해시태그가 생성되지 않은 공연
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
            max_tokens=150, # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
            temperature=0.7, # 모델 응답의 '창의성' 조절
            n=1, # 응답 개수
            stop=None # max_token 제한 도달할 때까지 토큰 생성
        )
        hashtags = response.choices[0].text.strip().split()[:3]
        performance.hashtags = " ".join(hashtags)  # 생성된 해시태그들을 string으로 저장
        performance.save()
        return performance.hashtags



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