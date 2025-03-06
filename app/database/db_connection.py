import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ✅ 프로젝트 루트 디렉토리 찾기
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ `DB.txt` 경로를 `config/` 폴더에 고정
DB_FILE_PATH = os.path.join(BASE_DIR, "config", "DB.txt")

# ✅ DB 연결 정보 불러오기
try:
    with open(DB_FILE_PATH, "r") as file:
        db_info = file.read().splitlines()

    DB_HOST = db_info[0]
    DB_PORT = db_info[1]
    DB_NAME = db_info[2]
    DB_USER = db_info[3]
    DB_PASSWORD = db_info[4]

    # ✅ MySQL 연결 문자열
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # ✅ SQLAlchemy 엔진 생성
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

    # ✅ 세션 팩토리 설정
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print("✅ DB 연결 성공!")

except Exception as e:
    print(f"❌ DB 연결 실패: {e}")
    engine = None
    SessionLocal = None

# ✅ DB 세션 생성 함수
def get_db():
    if SessionLocal is None:
        raise Exception("DB 연결이 설정되지 않았습니다.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
