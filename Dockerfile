# ✅ 1. Python 기반 FastAPI 실행을 위한 베이스 이미지 설정
FROM python:3.9-slim

# ✅ 2. 작업 디렉토리 설정
WORKDIR /app

# ✅ 3. 필요한 시스템 패키지 설치 (예: libGL 등)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# ✅ 4. Poetry 설치 (패키지 관리용)
RUN pip install --no-cache-dir poetry

# ✅ 5. 프로젝트 파일 복사
COPY pyproject.toml poetry.lock ./
COPY app/ app/

# ✅ 6. Poetry를 사용하여 의존성 설치
RUN poetry install --no-root --no-dev

# ✅ 7. 포트 설정 및 실행 명령어 지정
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]