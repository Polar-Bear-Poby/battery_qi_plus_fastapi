import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ✅ 프로젝트 루트 디렉토리 찾기
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ `.env` 파일 로드
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# ✅ DB 환경 변수 로드
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DB")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")

# ✅ MySQL 연결 문자열 생성
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ✅ SQLAlchemy 엔진 및 세션 설정
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    📌 요청마다 새로운 DB 세션을 생성하고, 요청이 끝나면 자동으로 닫음.
    """
    db = SessionLocal()
    try:
        yield db  # 요청이 끝날 때까지 세션 유지
    finally:
        db.close()  # 요청이 끝나면 세션 닫기
