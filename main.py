import uvicorn

if __name__ == "__main__":
    # 개발 서버 실행
    uvicorn.run(
        "app.api:app",  # 앱 모듈 경로
        host="localhost",  # 로컬에서 접근 가능
        port=8000,  # 포트 번호
        reload=True,  # 코드 변경시 자동 재시작
    )
