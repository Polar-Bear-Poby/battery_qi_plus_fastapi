import os
import json
from datetime import datetime
from typing import Dict
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.config.settings import RESULT_STORAGE_DIR
from app.config.settings import BUFFER_LIST

def select_global_buffer(buffer_id: str):
    """
    📌 C#에서 버퍼 ID를 입력하면 해당 버퍼 경로를 반환하는 함수
    - `buffer_id`: "buffer_1", "buffer_2", "buffer_3" 중 하나
    """
    return BUFFER_LIST.get(buffer_id, BUFFER_LIST["buffer_1"])  # 기본값은 `buffer_1`


def save_result_to_json(battery_id: str, result_data: Dict) -> str:
    """
    📌 AI 추론 결과를 JSON 파일로 저장
    - `battery_id`: 검사한 배터리 셀 ID
    - `result_data`: AI 추론 결과 데이터 (JSON 형태)
    - 반환값: 저장된 JSON 파일 경로
    """
    pass  # 이후 구현 예정

def save_result_to_db(battery_id: str, result_data: Dict, db: Session):
    """
    📌 AI 추론 결과를 MySQL DB에 저장
    - `battery_id`: 검사한 배터리 셀 ID
    - `result_data`: AI 추론 결과 데이터 (JSON 형태)
    - `db`: DB 세션 객체
    """
    pass  # 이후 구현 예정

def move_files_to_storage(battery_id: str):
    """
    📌 검사 완료된 이미지 및 JSON 결과를 대용량 저장장치로 이동
    - `battery_id`: 검사한 배터리 셀 ID
    """
    pass  # 이후 구현 예정
