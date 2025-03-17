import os
from dotenv import load_dotenv

# ✅ `.env` 파일 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "../.env")  # `.env`가 프로젝트 루트에 있다고 가정
load_dotenv(ENV_PATH)

# ✅ DB 환경 변수 설정
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DB")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")

# 폴더 A, B, C 경로를 환경 변수에서 불러오기
FOLDER_A = os.getenv("FOLDER_A_PATH", r"D:\2025_1\SF_Hard3_1st_project\arduino")  # 기본값 설정 가능
FOLDER_B = os.getenv("FOLDER_B_PATH", r"D:\2025_1\SF_Hard3_1st_project\image_from_arduino")
FOLDER_C = os.getenv("FOLDER_C_PATH", r"D:\2025_1\SF_Hard3_1st_project\Central_Storage")

