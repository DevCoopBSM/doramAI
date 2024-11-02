# Python 3.11.3 베이스 이미지 사용
FROM python:3.11.3-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt .

# 로컬에서 클론한 py-hanspell 디렉토리 복사
COPY py-hanspell ./py-hanspell

# FastAPI와 uvicorn 설치
RUN pip install --no-cache-dir fastapi uvicorn

# py-hanspell의 requirements.txt 설치
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r py-hanspell/requirements.txt

# py-hanspell의 setup.py 설치
RUN pip install --no-cache-dir ./py-hanspell

# 애플리케이션 코드 복사
COPY . .

# FastAPI 서버 실행
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]