from fastapi import APIRouter, Depends
from database.db_connection import get_db
import os
import signal
import time
import request
router = APIRouter()

@router.get("/shutdown")
def shutdown_server(db=Depends(get_db)):
    """
    DB에서 'OFF' 명령을 감지하면 FastAPI 서버를 안전하게 종료
    """
    # DB에서 상태 확인
    db.execute("SELECT status FROM server_status WHERE id=1")
    status = db.fetchone()

    if status and status[0] == "OFF":
        print("🛑 서버 종료 요청 감지. 현재 작업을 마무리하고 종료합니다...")

        # AI 모델의 현재 진행 중인 작업 마무리
        cleanup_tasks()

        # FastAPI 서버 종료
        os.kill(os.getpid(), signal.SIGINT)

        return {"message": "FastAPI 서버 종료 중..."}
    return {"message": "서버는 계속 실행 중"}

def cleanup_tasks():
    """
    AI 모델 및 데이터 처리 작업 마무리
    """
    print("✅ 현재 진행 중인 AI 추론 및 데이터 전송 작업을 마무리하는 중...")
    time.sleep(5)  # 가상 작업 종료 대기 (실제 작업 대기 코드 필요)
    print("✅ 모든 작업이 완료됨. 서버를 종료합니다.")

@router.post("/shutdown")
def shutdown_system():
    """
    📌 C# 프로그램에게 HTTP 요청을 보내 아두이노 전송 중지 명령 실행
    """
    try:
        response = requests.post("http://127.0.0.1:5000/shutdown")
        if response.status_code == 200:
            return {"message": "Shutdown command sent to C#."}
        else:
            return {"error": f"Failed to shutdown: {response.text}"}
    except Exception as e:
        return {"error": f"Failed to communicate with C#: {e}"}