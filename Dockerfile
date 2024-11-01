# doramAI/Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# FastAPI 서버 실행
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]