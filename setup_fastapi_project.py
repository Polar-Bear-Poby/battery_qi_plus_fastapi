import os

# 프로젝트 루트 디렉터리
PROJECT_NAME = "battery_qi_fastapi"
BASE_DIR = os.path.join(os.getcwd(), PROJECT_NAME)

# 프로젝트 폴더 구조 정의
folders = [
    "app",
    "app/routers",
    "app/services",
    "app/models",
    "app/utils",
    "app/database",
    "app/data",  # 이미지 저장 폴더 (아두이노 → FastAPI)
    "app/logs",  # 로그 저장 폴더
    "tests",
]

# 기본 파일 생성 (FastAPI 엔트리포인트, 설정 파일)
files = [
    "app/main.py",
    "app/routers/__init__.py",
    "app/routers/predict.py",
    "app/routers/upload.py",
    "app/routers/health.py",
    "app/routers/shutdown.py",
    "app/routers/status.py",
    "app/services/__init__.py",
    "app/services/file_manager.py",
    "app/services/inference.py",
    "app/models/__init__.py",
    "app/models/model.py",
    "app/utils/__init__.py",
    "app/utils/database.py",
    "app/utils/storage_manager.py",
    "app/database/__init__.py",
    "app/database/db_connection.py",
    "app/logs/app.log",
    "tests/__init__.py",
    "tests/test_api.py",
    "requirements.txt",
    "Dockerfile",
]

# 폴더 생성
for folder in folders:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

# 파일 생성
for file in files:
    full_path = os.path.join(BASE_DIR, file)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("")  # 빈 파일 생성

print(f"✅ FastAPI 프로젝트 '{PROJECT_NAME}' 폴더 및 파일 생성 완료!")
