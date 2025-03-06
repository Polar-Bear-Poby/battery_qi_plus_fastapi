from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import os
from app.database.db_connection import get_db

router = APIRouter()

# ✅ 글로벌 버퍼를 FastAPI 내부가 아닌, 별도의 저장 장치로 설정
GLOBAL_BUFFER_DIR = "D:/global_buffer"  # 네가 원하는 실제 경로로 변경 가능

@router.post("/upload/")
async def upload_file(
    battery_id: str = Form(...),
    angle: str = Form(...),  # 촬영각도 A 또는 B
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    📌 배터리 셀 이미지 업로드 API (별도의 저장 장치에 저장)
    - `battery_id` : 배터리 셀 ID
    - `angle` : 촬영각도 (A 또는 B)
    - `file` : 업로드할 이미지 파일
    """

    # ✅ 글로벌 버퍼의 올바른 저장 경로 설정
    save_dir = os.path.join(GLOBAL_BUFFER_DIR, battery_id, angle)
    os.makedirs(save_dir, exist_ok=True)  # 폴더 없으면 생성

    # 파일 저장 경로
    file_path = os.path.join(save_dir, file.filename)

    # 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # DB에 파일 저장 정보 기록
    db.execute(
        "INSERT INTO uploads (battery_id, angle, file_path) VALUES (:battery_id, :angle, :file_path)",
        {"battery_id": battery_id, "angle": angle, "file_path": file_path},
    )
    db.commit()

    return {"message": "File uploaded successfully", "battery_id": battery_id, "file_path": file_path}
