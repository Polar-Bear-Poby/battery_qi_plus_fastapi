from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db_connection import get_db  # DB 세션 종속성
from services.file_manager import analyze_results_store_and_move

router = APIRouter()

@router.post("/analyze-and-upload/{battery_id}")
def analyze_and_upload(battery_id: int, db: Session = Depends(get_db)):
    """
    📌 검사 결과를 분석하고, DB에 저장한 후, 대용량 저장장치(C)로 이동
    - `battery_id`: 검사할 배터리 셀 ID
    - `db`: SQLAlchemy 세션 (FastAPI 종속성 사용)
    """
    try:
        analyze_results_store_and_move(str(battery_id), db)
        return {"message": f"배터리 {battery_id} 검사 분석 및 저장 완료"}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
