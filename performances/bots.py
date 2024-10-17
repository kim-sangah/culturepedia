from django.conf import settings
from openai import OpenAI
import openai
from .models import Performance, Hashtag
from django.db.models import Q
from PIL import Image
import pytesseract
import requests
from io import BytesIO
import base64

CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY,)
MAX_FILE_SIZE_MB = 10

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# 사용자가 리뷰하거나 찜한 공연들의 해시태그와 입력받은 해시태그를 바탕으로 공연 추천 (openai 사용)
# def generate_recommendations(user_preferences, input_tags):
#     # user_preferences에 있는 공연들을 context로 줌
#     # context = f"User is interested in the following performances: {', '.join(user_preferences)}\n"

#     # user_preferences에 있는 공연들의 해시태그를 context로 줌
#     preferred_hashtags = []
#     for performance in user_preferences:
#         preferred_hashtags.append(performance.performance_hashtags)

#     context = f"These are the hashtags of performances the user is interested in: {', '.join(preferred_hashtags)}\n"

#     # input_tags가 있을 경우, input_tags를 context에 추가
#     if input_tags:
#         context += f"These are the tags the user has additionally selected: {', '.join(input_tags)}\n"

#     # 공연중, 공연예정인 공연들을 performance_list로 줌
#     performance_list = Performance.objects.filter(
#         Q(state="공연중") | Q(state="공연예정"))

#     # performance_list에 있는 각 공연들의 제목과 공연 종류, 줄거리, 해시태그를 context로 줌
#     for performance in performance_list:
#         context += f"Performance: {performance['title']}, Type: {performance['type']}, Synopsis: {performance['synopsis']}, Hashtags: {performance['performance_hashtag']}\n"

#     prompt = context + "Based on the tags in preffered_tags and the selected tags in input_tags, recommend performances for the user in Korean."
#     response = openai.Completion.create(
#         engine="gpt-4o-mini",
#         prompt=prompt,
#         max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
#         temperature=0.7,  # 모델 응답의 '창의성' 조절
#         n=1,  # 응답 개수
#         stop=None  # max_token 제한 도달할 때까지 토큰 생성
#     )

#     return response.choices[0].text.strip()


# 사용자가 리뷰하거나 찜한 공연들의 해시태그와 입력받은 해시태그를 바탕으로 공연 추천 (openai 사용 X)
def generate_recommendations(user_preferences, input_tags):
    # user_preferences에 있는 선호하는 공연들의 해시태그를 preferred_hashtags 리스트에 넣음
    preferred_hashtags = set()
    for performance in user_preferences:
        preferred_hashtags.update(performance.performance_hashtags)

    # input_tags가 있을 경우, input_tags를 preferred_hashtags에 추가
    if input_tags:
        preferred_hashtags.update(input_tags)

    # 공연중, 공연예정인 공연들을 performance_list에 넣음
    performance_list = Performance.objects.filter(
        Q(state="공연중") | Q(state="공연예정")
    )

    recommended_performances = []

    # performance_list에 있는 공연의 해시태그들 중 2개 이상이 preferred_hashtags에 있는 해시태그들과 일치하는지 체크
    for performance in performance_list:
        performance_hashtags = set(performance.performance_hashtags)
        common_hashtags = preferred_hashtags.intersection(performance_hashtags)

        if len(common_hashtags) >= 2:
            recommended_performances.append({
                "title": performance['title'],
                "state": performance['state'],
                "type": performance['type'],
                "poster": performance['poster'],
                "hashtags": performance['performance_hashtags'],
            })

    return recommended_performances


# # 데이터가 없는(리뷰를 작성하거나 찜한 공연이 없는) 사용자로부터 입력받은 해시태그로만 공연 추천
# def generate_recommendations_with_tags(input_tags):
#     context = f"These are the tags the user has selected: {', '.join(input_tags)}\n"

#     # 공연중, 공연예정인 공연들을 performance_list로 줌
#     performance_list = Performance.objects.filter(
#         Q(state="공연중") | Q(state="공연예정"))

#     # performance_list에 있는 각 공연들의 제목과 공연 종류, 줄거리, 해시태그를 context로 줌
#     for performance in performance_list:
#         context += f"Performance: {performance['title']}, Type: {performance['type']}, Synopsis: {performance['synopsis']}, Hashtags: {performance['performance_hashtag']}\n"

#     prompt = context + \
#         "Based on the selected tags in input_tags, recommend performances for the user in Korean."
#     response = openai.Completion.create(
#         engine="gpt-4o-mini",
#         prompt=prompt,
#         max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
#         temperature=0.7,  # 모델 응답의 '창의성' 조절
#         n=1,  # 응답 개수
#         stop=None  # max_token 제한 도달할 때까지 토큰 생성
#     )

#     return response.choices[0].text.strip()


# 데이터가 없는(리뷰를 작성하거나 찜한 공연이 없는) 사용자로부터 입력받은 해시태그로만 공연 추천 (openai 사용 X)
def generate_recommendations_with_tags(input_tags):
    # 유저에게 입력받은 태그들을 set()로 저장
    input_tags_set = set(input_tags)

    # 공연중, 공연예정인 공연들을 performance_list에 넣음
    performance_list = Performance.objects.filter(
        Q(state="공연중") | Q(state="공연예정")
    )

    recommended_performances = []

    # performance_list에 있는 공연의 해시태그들 중 2개 이상이 input_tags_set에 있는 해시태그들과 일치하는지 체크
    for performance in performance_list:
        performance_hashtags = set(
            performance.performance_hashtag.values_list('name', flat=True))
        common_hashtags = input_tags_set.intersection(performance_hashtags)

        if len(common_hashtags) >= 2:
            recommended_performances.append({
                "kopis_id": performance.kopis_id,
                "title": performance.title,
                "state": performance.state,
                "type": performance.type,
                "poster": performance.poster,
                "hashtags": performance.performance_hashtag.values_list('name', flat=True),
            })

    return recommended_performances

# 줄거리 생성
# def generate_synopsis(performance):
#     # 줄거리가 없는 공연의 소개이미지나 포스터에 있는 글 추출해 줄거리(공연 설명) 생성
#     styurls_text = ""

#     if performance.styurls and not performance.synopsis:  # 소개이미지가 있는 경우
#         for styurl in performance.styurls:
#             try:
#                 response = requests.get(styurl)
#                 response.raise_for_status()

#                 image = Image.open(BytesIO(response.content))

#                 text = pytesseract.image_to_string(
#                     image, lang='kor+eng', timeout=3)
#                 if text.strip():  # 추출된 텍스트가 비어있지 않은지 체크
#                     styurls_text += text
#                 else:
#                     return "소개이미지에서 텍스트를 추출할 수 없습니다."
#             except RuntimeError as TimeoutError:
#                 print(f"Error occurred while processing image: {TimeoutError}")
#                 continue
#             except FileNotFoundError:
#                 print(f"File not found: {styurl}")
#                 continue
#             except Exception as e:
#                 print(f"An unexpected error occurred: {e}")
#                 continue

#         context = f"This is the Korean text embedded in a descriptive image of a performance: {styurls_text}\n"
#         prompt = context + \
#             "Based on the text, generate a concise synopsis or a description of the performance in Korean."

#         response = openai.Completion.create(
#             engine="gpt-4o-mini",
#             prompt=prompt,
#             max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
#             temperature=0.7,  # 모델 응답의 '창의성' 조절
#             n=1,  # 응답 개수
#             stop=None  # max_token 제한 도달할 때까지 토큰 생성
#         )
#         # 생성된 synopsis를 string으로 저장
#         performance.synopsis = response.choices[0].text.strip()
#     elif performance.poster and not performance.synopsis:  # 소개이미지는 없고 포스터는 있는 경우
#         try:
#             poster_text = pytesseract.image_to_string(
#                 Image.open(performance.poster), lang='kor+eng', timeout=3)
#             if poster_text.strip():  # 추출된 텍스트가 비어있지 않은지 체크
#                 context = f"This is the Korean text embedded in a performance's poster: {poster_text}\n"
#                 prompt = context + \
#                     "Based on the text, generate a concise synopsis or a description of the performance in Korean."

#                 response = openai.Completion.create(
#                     engine="gpt-4o-mini",
#                     prompt=prompt,
#                     max_tokens=150,  # 응답의 token 수 제한 (한 문장은 보통 토큰 10~20개)
#                     temperature=0.7,  # 모델 응답의 '창의성' 조절
#                     n=1,  # 응답 개수
#                     stop=None  # max_token 제한 도달할 때까지 토큰 생성
#                 )
#                 # 생성된 synopsis를 string으로 저장
#                 performance.synopsis = response.choices[0].text.strip()
#             else:
#                 return "포스터에서 텍스트를 추출할 수 없습니다."
#         except RuntimeError as TimeoutError:
#             print(f"Error occurred while processing poster: {TimeoutError}")
#     else:  # 소개 이미지도 없고 포스터도 없는 경우
#         return "줄거리를 생성할 수 없습니다."


# 해시태그 생성
def generate_hashtags_for_performance(performance):
    information = ''
    images_url = []        # 이미지 경로
    hashtag_list = '#극적인, #내한공연, #시각예술, #감동적, #라이브음악, #실험적, #웅장한, #가족친화적, #이머시브, #화려한, #전통적, #컴팩트한공연장, #트렌디한, #로맨틱, #창의적, #코믹한, #미스터리, #어두운, #힐링, #신나는'
    # 공연의 필드 일부를 정보로 주고 이를 바탕으로 해시태그를 생성하게 함
    if performance.title:
        information += f'title: {performance.title},'
    if performance.type:
        information += f'type: {performance.type},'
    if performance.synopsis:
        information += f'synopsis: {performance.synopsis}'
    if performance.poster:
        images_url.append(performance.poster)
    if performance.styurls:
        if isinstance(performance.styurls["styurl"], list):
            images_url.extend(performance.styurls["styurl"])
        else:
            images_url.append(performance.styurls["styurl"])

    images_path = []

    for url in images_url:
        file_name = url.split('/')[-1]
        file_path = f"./static/img/{performance.kopis_id}/{file_name}"
        images_path.append(file_path)

    # 이미지 데이터를 Base64로 인코딩
    base64_images = []
    for image_path in images_path:
        # 파일 확장자에 따라 MIME 타입 설정
        image_path_lower = image_path.lower()
        # 파일 확장자에 따라 MIME 타입 설정
        if image_path_lower.endswith(".gif"):
            mime_type = "image/gif"
        elif image_path_lower.endswith(".jpg") or image_path_lower.endswith(".jpeg") or image_path_lower.endswith(".jfif"):
            mime_type = "image/jpeg"
        elif image_path_lower.endswith(".png"):
            mime_type = "image/png"
        elif image_path_lower.endswith(".bmp"):
            mime_type = "image/bmp"
        elif image_path_lower.endswith(".webp"):
            mime_type = "image/webp"
        elif image_path_lower.endswith(".tiff") or image_path_lower.endswith(".tif"):
            mime_type = "image/tiff"
        elif image_path_lower.endswith(".svg"):
            mime_type = "image/svg+xml"
        elif image_path_lower.endswith(".ico"):
            mime_type = "image/vnd.microsoft.icon"
        elif image_path_lower.endswith(".heic") or image_path_lower.endswith(".heif"):
            mime_type = "image/heif"
        else:
            mime_type = "application/octet-stream"  # Unknown type

        with open(image_path, "rb") as image_file:
            base64_encoded_image = base64.b64encode(
                image_file.read()).decode('utf-8')
            base64_images.append(
                f"data:{mime_type};base64,{base64_encoded_image}")

    # OpenAI API 요청
        # for styurl in performance.styurls:
        #     file_size_mb = get_file_size(styurl)
        #     if file_size_mb <= MAX_FILE_SIZE_MB:  # 10 MB보다 작거나 같은 크기의 이미지만 append
        #         images_path.append({styurl})
        #     else:
        #         print(f"Image {styurl} is larger than {MAX_FILE_SIZE_MB} MB and has been excluded.")

    response = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"Select all appropriate hashtags ({hashtag_list}) based on the images and information provided: {information}. Just provide the hashtags."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please check the following image and select all appropriate tags."
                    },
                    *[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_images[i]
                            }
                        }
                        for i in range(len(base64_images))
                    ],
                ]
            },
        ],
        max_tokens=150,  # 응답의 token 수 제한
        temperature=0.7,  # 모델 응답의 '창의성' 조절
        n=1,  # 응답 개수
    )

    hashtags = response.choices[0].message.content.strip().split()
    print(hashtags)
    for tag in hashtags:
        tag = tag.strip('#')
        Hashtag(performance_api_id=performance, name=tag).save()
    return performance.performance_hashtag.all()

# 소개이미지 파일 사이즈 받기
# def get_file_size(url):
#     try:
#         response = requests.get(url, stream=True)

#         total_size = 0

#         # chunk로 나눠진 response를 돌아 각 chunk를 총 크기에 더함 (기본 chunk 사이즈는 1024 바이트)
#         for chunk in response.iter_content(chunk_size=1024):
#             total_size += len(chunk)

#         # 파일 크기 단위를 바이트에서 메가바이트로 변환
#         file_size_mb = total_size / (1024 * 1024)

#         return file_size_mb
#     except requests.RequestException as e:
#         print(f"Error fetching file size for {url}: {e}")
#         return 0

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
