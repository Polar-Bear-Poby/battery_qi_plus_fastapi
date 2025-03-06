from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 라우터 import
from app.routers import health, upload, predict, shutdown, status

app = FastAPI(title="Battery Quality Inspection API", version="1.0")

# # CORS 설정 (CORS가 필요한 경우)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 모든 도메인 허용 (보안 강화 필요 시 특정 도메인만 허용)
#     allow_credentials=True,
#     allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
#     allow_headers=["*"],  # 모든 HTTP 헤더 허용
# )

# 라우터 등록
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(shutdown.router, prefix="/shutdown", tags=["Shutdown"])
app.include_router(status.router, prefix="/status", tags=["Status"])

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
