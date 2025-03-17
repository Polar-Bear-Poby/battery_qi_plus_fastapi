from fastapi import APIRouter, HTTPException
from services.inference import predict_image
import os
from config.settings import FOLDER_B

router = APIRouter()

@router.post("/predict/{battery_id}")
async def run_prediction(battery_id: str):
    """
    📌 배터리 셀 ID를 받아 해당 ID의 이미지를 AI 추론 수행
    📌 폴더 B/{battery_id}에서 0°, 90°, 180°, 270°의 이미지를 가져와 추론
    📌 추론 결과는 해당 배터리 셀 ID의 `result` 폴더에 저장됨
    """

    # ✅ 배터리 셀 ID 폴더 경로
    battery_folder = os.path.join(FOLDER_B, battery_id)

    # ✅ 폴더가 존재하는지 확인
    if not os.path.exists(battery_folder):
        raise HTTPException(status_code=404, detail=f"배터리 {battery_id} 폴더가 {battery_folder} 존재하지 않습니다.")

    # ✅ AI 추론할 이미지 선택 (0°, 90°, 180°, 270°)
    image_paths = []
    valid_angles = {"0", "90", "180", "270"}
    png_lists = [f for f in os.listdir(battery_folder) if f.endswith(".png")]
    for file_name in png_lists:
        file_parts = file_name.split("_")  # 파일명을 '_' 기준으로 분할
        angle_part = file_parts[-1].replace(".png", "")  # 마지막 부분이 각도 정보
        if angle_part in valid_angles:
            image_paths.append(os.path.join(battery_folder, file_name))

    # ✅ 이미지가 충분한지 확인
    if len(image_paths) != 8:
        print(f"{battery_id} 폴더에 필요한 8장의 이미지가 부족합니다. 현재 {len(image_paths)}장 존재")

    # ✅ AI 추론 실행
    result_folder = os.path.join(battery_folder, "result")
    os.makedirs(result_folder, exist_ok=True)  # 결과 저장 폴더 생성
    results = []
    for image_path in image_paths:
        result = predict_image(image_path, result_folder)
        results.append(result)

    return {"message": f"배터리 {battery_id} AI 추론 완료", "results": results}
