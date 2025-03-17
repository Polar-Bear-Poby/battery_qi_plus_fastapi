import asyncio
import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.folder_watcher import watch_folder_A, watch_folder_B_result, print_queue_status
from database.db_connection import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    📌 FastAPI 서버 시작 시 백그라운드 작업 실행 & 종료 시 정리
    📌 폴더 A 감시기, 폴더 B 감시기 실행
    📌 DB 관리 테이블을 주기적으로 확인하여 'off' 명령 감지 시 graceful shutdown 실행
    """
    task_A = asyncio.create_task(watch_folder_A())  # 🚀 폴더 A 감시 (촬영 완료 감지 & AI 추론 요청)
    task_B = asyncio.create_task(watch_folder_B_result())  # 🚀 폴더 B 감시 (AI 결과 저장 감지 & Upload 요청)
    # task_db_check = asyncio.create_task(check_db_for_shutdown(app))  # 🚀 DB 체크 감시 시작
    task_queue_status = asyncio.create_task(print_queue_status())  # ✅ 큐 상태 출력 추가
    yield  # FastAPI 서버 실행

    # ✅ 서버 종료 시 백그라운드 작업 정리
    task_A.cancel()
    task_B.cancel()
    # task_db_check.cancel()
    task_queue_status.cancel()  # ✅ 큐 상태 출력 작업도 종료
    print("⚠ FastAPI 서버 종료")

# async def check_db_for_shutdown(app: FastAPI):
#     """
#     📌 주기적으로 DB 관리 테이블을 확인하여 'off' 명령 감지 시 FastAPI graceful shutdown 실행
#     """
#     while True:
#         try:
#             async with get_db() as db:
#                 result = await db.execute("SELECT status FROM management_table WHERE id=1")  # 🔹 예시 쿼리
#                 status = result.fetchone()[0]  # 🔹 관리 테이블에서 상태 확인
#
#                 if status == "off":
#                     print("⚠ 'off' 명령 감지됨 → FastAPI 서버 종료 준비")
#
#                     # ✅ FastAPI 서버 종료
#                     loop = asyncio.get_running_loop()
#                     loop.stop()
#                     sys.exit(0)  # 🔹 FastAPI 프로세스 종료
#         except Exception as e:
#             print(f"❌ DB 연결 또는 조회 실패: {e}")
#
#         await asyncio.sleep(30)  # 🔹 30초마다 DB 확인 (필요에 따라 조정 가능)

# ✅ FastAPI 인스턴스 생성
app = FastAPI(lifespan=lifespan)

# ✅ 라우터 등록
from routers import status, predict, upload
app.include_router(status.router)
app.include_router(predict.router)
app.include_router(upload.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
