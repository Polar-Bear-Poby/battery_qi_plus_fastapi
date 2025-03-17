import os

# 프로젝트 루트 디렉터리
PROJECT_NAME = "battery_qi_fastapi"
BASE_DIR = os.path.join(os.getcwd(), PROJECT_NAME)

# 프로젝트 폴더 구조 정의
folders = [
    "routers",
    "services",
    "ai"
    "utils",
    "database",
]

# 기본 파일 생성 (FastAPI 엔트리포인트, 설정 파일)
files = [
    "main.py",
    "routers/__init__.py",
    "routers/predict.py",
    "routers/upload.py",
    "routers/health.py",
    "routers/shutdown.py",
    "routers/status.py",
    "services/__init__.py",
    "services/file_manager.py",
    "services/inference.py",
    "utils/__init__.py",
    "utils/database.py",
    "utils/image_processing.py",
    "utils/json_handler.py",
    "database/__init__.py",
    "database/db_connection.py",
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
