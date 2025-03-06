from fastapi import APIRouter, UploadFile, File
from ai.dataloaders.utils import load_image  # 이미지 변환 유틸리티
from app.services.inference import predict_images

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """이미지를 받아서 AI 모델 추론을 수행하는 FastAPI 엔드포인트"""
    image = load_image(await file.read())  # ✅ 이미지 변환
    preds = predict_images([image])  # ✅ AI 추론 수행
    return {"prediction": preds[0].tolist()}
