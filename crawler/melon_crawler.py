## 크롤링 코드
import requests
from bs4 import BeautifulSoup
import json
import os


# 멜론 차트 Top100 데이터 크롤링하는 함수
# 타입힌팅: 해당 변수의 데이터타입을 지정
def crawl_melon_chart(url: str) -> list[dict]:
    """
    멜론 차트 Top100 데이터 크롤링하는 함수
    Args:
      - url: 크롤링한 페이지 url
    Returns:
      - list: 크롤링한 데이터 리스트로 반환
    """

    # 브라우저 헤더 설정 (멜론은 User-Agent 체크함)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 웹페이지 요청
    response = requests.get(url, headers=headers)
    # print(f"response: {response}")

    # 데이터 추출(파싱)
    soup = BeautifulSoup(response.content, "lxml")

    # 순위별 곡 정보
    song_row_tags = soup.select("tbody tr")
    # print(f"갯수: {len(song_row_tags)}")

    # 수집된 차트 데이터
    chart_data = []

    for row_tag in song_row_tags:

        # 노래 ID값 추출
        id = int(row_tag.get("data-song-no"))

        # 순위 추출
        rank_tag = row_tag.select_one(".rank")
        rank = int(rank_tag.text.strip())

        # print(f"id: {id} - rank: {rank}")

        # 곡명 추출
        title_tag = row_tag.select_one(".ellipsis.rank01 a")
        title = title_tag.text.strip() if title_tag else "정보 없음"

        # 아티스트 추출
        artist_tags = row_tag.select(".ellipsis.rank02 > a")
        if artist_tags:
            # 여러 아티스트가 있을 경우 쉼표로 연결
            artists = [tag.text.strip() for tag in artist_tags]
            artist = ", ".join(artists)
        else:
            artist = "정보 없음"

        # 앨범명 추출
        album_tag = row_tag.select_one(".ellipsis.rank03 a")
        album = album_tag.text.strip() if album_tag else "정보 없음"

        # 데이터 가공
        song_info = {
            "id": id,
            "rank": rank,
            "title": title,
            "artist": artist,
            "album": album,
        }

        chart_data.append(song_info)

    return chart_data


# 데이터를 Json파일로 저장하는 함수
def save_to_json(data, filename="melon_chart_top100.json"):
    """크롤링한 데이터를 JSON 파일로 저장"""
    # 현재 파일 위치
    current_dir = os.path.dirname(__file__)  # crawler 폴더
    # 프로젝트 루트
    project_root = os.path.dirname(current_dir)  # playlist-class 폴더
    # data 폴더 경로
    data_dir = os.path.join(project_root, "app", "data")

    # 폴더 생성
    os.makedirs(data_dir, exist_ok=True)

    # 파일 경로
    file_path = os.path.join(data_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 파일 저장 완료: {filename}")
    except Exception as e:
        print(f"❌ JSON 파일 저장 실패: {e}")


if __name__ == "__main__":

    # 멜론 차트 크롤링
    melon_chart = crawl_melon_chart("https://www.melon.com/chart/index.htm")
    print(f"갯수: {len(melon_chart)}")
    print(melon_chart[0])

    if melon_chart:
        # JSON 파일로 저장
        save_to_json(melon_chart)
    else:
        print("❌ 크롤링 실패! 데이터를 수집하지 못했습니다.")
