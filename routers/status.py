from fastapi import APIRouter

router = APIRouter()

# ✅ FastAPI 서버 상태 (초기값: IDLE)
server_state = {"status": "IDLE"}

@router.get("/")
def get_status():
    """
    현재 FastAPI 서버 상태 반환
    """
    return {"server_status": server_state["status"]}

@router.post("/set_status/{new_status}")
def set_status(new_status: str):
    """
    FastAPI 상태를 변경하는 API (C# 또는 내부 로직에서 호출)
    상태 변경 가능:
    - IDLE → PROCESSING → OFF_PENDING → OFF
    """
    valid_states = ["IDLE", "PROCESSING", "OFF_PENDING", "OFF"]

    if new_status not in valid_states:
        return {"error": f"'{new_status}'는 올바른 상태가 아닙니다. 사용 가능한 상태: {valid_states}"}

    # 🚀 상태 변경 처리
    server_state["status"] = new_status
    return {"message": f"FastAPI 상태가 '{new_status}'로 변경되었습니다."}

@router.post("/restart")
def restart_server():
    """
    C#이 검사 라인을 다시 시작할 때, FastAPI를 다시 활성화하는 API
    """
    if server_state["status"] == "OFF":
        server_state["status"] = "IDLE"
        return {"message": "FastAPI가 다시 활성화되었습니다. 검사 가능."}
    return {"message": "FastAPI는 이미 실행 중입니다."}
