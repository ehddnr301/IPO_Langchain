import os
import requests
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


def search_naver_blog(
    query: str, sort: str = "accuracy", page: int = 1, size: int = 20
) -> Dict:
    """
    Kakao 블로그 검색 API를 사용하여 블로그 정보를 검색합니다.

    Parameters:
        api_key (str): Kakao REST API 키
        query (str): 검색할 쿼리
        sort (str): 정렬 방법 (accuracy, recency)
        page (int): 페이지 번호
        size (int): 한 페이지에 표시할 레코드 수

    Returns:
        Dict: API 응답을 포함하는 딕셔너리
    """

    # HTTP 헤더에 Authorization을 추가합니다.
    headers = {"Authorization": f"KakaoAK {os.getenv('KAKAO_API_KEY')}"}

    # API 요청 URL과 파라미터를 설정합니다.
    url = "https://dapi.kakao.com/v2/search/blog"
    params = {"sort": sort, "page": page, "size": size, "query": query}

    # GET 요청을 보냅니다.
    response = requests.get(url, headers=headers, params=params)

    # 결과를 확인합니다.
    if response.status_code == 200:
        return response.json()
    else:
        return {"Error": response.status_code}
