from django.conf import settings
from openai import OpenAI
import openai
from .models import Performance
from django.db.models import Q
from PIL import Image
import pytesseract
import requests
from io import BytesIO
CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY,)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# 사용자가 리뷰하거나 찜한 공연들의 해시태그와 입력받은 해시태그를 바탕으로 공연 추천
def generate_recommendations(user_preferences, input_tags):
    # user_preferences에 있는 공연들을 context로 줌
    # context = f"User is interested in the following performances: {', '.join(user_preferences)}\n"

    # user_preferences에 있는 공연들의 해시태그를 context로 줌
    preferred_hashtags = []
    for performance in user_preferences:
        preferred_hashtags.append(performance.performance_hashtags)

    context = f"These are the hashtags of performances the user is interested in: {', '.join(preferred_hashtags)}\n"

    # input_tags가 있을 경우, input_tags를 context에 추가
    if input_tags:
        context += f"These are the tags the user has additionally selected: {', '.join(input_tags)}\n"

    # 공연중, 공연예정인 공연들을 performance_list로 줌
    performance_list = Performance.objects.filter(
        Q(state="공연중") | Q(state="공연예정"))

    # performance_list에 있는 각 공연들의 제목과 공연 종류, 줄거리, 해시태그를 context로 줌
    for performance in performance_list:
        context += f"Performance: {performance['title']}, Type: {performance['type']}, Synopsis: {performance['synopsis']}, Hashtags: {performance['performance_hashtag']}\n"

    prompt = context + "Based on the tags in preffered_tags and the selected tags in input_tags, recommend performances for the user in Korean."
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
        context += f"Performance: {performance['title']}, Type: {performance['type']}, Synopsis: {performance['synopsis']}, Hashtags: {performance['performance_hashtag']}\n"

    prompt = context + \
        "Based on the selected tags in input_tags, recommend performances for the user in Korean."
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
    styurls_text = ""

    if performance.styurls and not performance.synopsis: # 소개이미지가 있는 경우
        for styurl in performance.styurls:
            try:
                response = requests.get(styurl)
                response.raise_for_status()

                image = Image.open(BytesIO(response.content))

                text = pytesseract.image_to_string(image, lang='kor+eng', timeout=3)
                if text.strip(): # 추출된 텍스트가 비어있지 않은지 체크
                    styurls_text += text
                else:
                    return "소개이미지에서 텍스트를 추출할 수 없습니다."
            except RuntimeError as TimeoutError:
                print(f"Error occurred while processing image: {TimeoutError}")
                continue
            except FileNotFoundError:
                print(f"File not found: {styurl}")
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                continue

        context = f"This is the Korean text embedded in a descriptive image of a performance: {styurls_text}\n"
        prompt = context + \
            "Based on the text, generate a concise synopsis or a description of the performance in Korean."

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
                context = f"This is the Korean text embedded in a performance's poster: {poster_text}\n"
                prompt = context + \
                "Based on the text, generate a concise synopsis or a description of the performance in Korean."

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
    question = ''
    images = []
    hashtag_list = ''
    # 공연의 필드 일부를 정보로 주고 이를 바탕으로 해시태그를 생성하게 함
    if performance.title:
        question += f'title: {performance.title},'
    if performance.type:
        question += f'type: {performance.type},'
    if performance.synopsis:
        question += f'synopsis: {performance.synopsis}'
    if performance.poster:
        images.append({performance.poster})
    if performance.styurls:
        images.append({performance.styurls})
        
    context = f"These are available informations of a performance in Korean: {question}"

    response = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "This is a helper that helps you choose appropriate hashtags."
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please select the appropriate hashtag among {hashtag_list} based on the images and information provided: {context}"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": images
                        }
                    }
                ]
            },
        ],
        max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
        temperature=0.7,  # 모델 응답의 '창의성' 조절
        n=1,  # 응답 개수
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
