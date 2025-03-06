import os
from dotenv import load_dotenv

# ✅ `.env` 파일 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 `settings.py`가 있는 폴더 (`config/`)
ENV_PATH = os.path.join(BASE_DIR, ".env")  # `.env` 파일 경로
load_dotenv(ENV_PATH)  # `.env` 파일 로드

# ✅ AI 모델 가중치 파일 경로
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(BASE_DIR, "..", "models", "battery_qi_model.pt"))

# ✅ 글로벌 버퍼 리스트
BUFFER_LIST = {
    "buffer_1": os.getenv("BUFFER_1", "D:/buffer_1"),
    "buffer_2": os.getenv("BUFFER_2", "D:/buffer_2"),
    "buffer_3": os.getenv("BUFFER_3", "D:/buffer_3")
}

# ✅ 기본 글로벌 버퍼 설정
GLOBAL_BUFFER_DIR = os.getenv("GLOBAL_BUFFER_DIR", BUFFER_LIST["buffer_1"])

# ✅ AI 추론 결과 JSON 저장 경로
RESULT_STORAGE_DIR = os.getenv("RESULT_STORAGE_DIR", "D:/result_storage")

# ✅ 대용량 저장장치 경로
LARGE_STORAGE_DIR = os.getenv("LARGE_STORAGE_DIR", "D:/large_storage")

# ✅ 확인용 출력 (개발 시 확인하고, 운영 환경에서는 제거 가능)
if __name__ == "__main__":
    print(f"✅ MODEL_PATH: {MODEL_PATH}")
    print(f"✅ BUFFER_LIST: {BUFFER_LIST}")
    print(f"✅ GLOBAL_BUFFER_DIR: {GLOBAL_BUFFER_DIR}")
    print(f"✅ RESULT_STORAGE_DIR: {RESULT_STORAGE_DIR}")
    print(f"✅ LARGE_STORAGE_DIR: {LARGE_STORAGE_DIR}")
