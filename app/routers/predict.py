from fastapi import APIRouter, HTTPException
from app.services.inference import run_inference

router = APIRouter()

@router.get("/predict/{battery_id}")
async def predict_battery_qi(battery_id: str):
    """
    📌 배터리 셀 ID를 입력받아 AI 추론을 수행하는 API
    - `battery_id`: 검사할 배터리 셀 ID
    - AI 추론 결과를 JSON 형태로 반환
    """
    # ✅ AI 추론 실행
    result = run_inference(battery_id)

    # ✅ 에러 발생 시 예외 처리
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result  # JSON 응답
