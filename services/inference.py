import torch
from torchvision import transforms
from PIL import Image
import numpy as np
from services.model_loader import get_model
from utils.image_processing import extract_contour_coordinates, add_pr_outline
from utils.json_handler import save_pr_json
import os

# ✅ 슬라이딩 윈도우 설정
CROP_SIZE = 640
OFFSET = 400

def transform_image(image):
    transform = transforms.Compose([
        transforms.ToTensor(),  # PIL 이미지를 PyTorch 텐서로 변환
        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))  # 정규화
    ])
    return transform(image)

def predict_image(image_path: str, result_folder: str):
    """
    📌 AI 모델을 사용하여 여러 배터리 셀 이미지 추론 수행
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = get_model()  # ✅ 모델을 한 번만 로드하도록 개선
    # model.to(device)
    # model.eval()

    try:
        # ✅ 이미지 로드 및 전처리 (1920x1080 전체 변환)
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform_image(image).unsqueeze(0).to(device)  # ✅ 변환 & 배치 차원 추가
        _, _, height, width = input_tensor.shape  # 채널, 높이, 너비 가져오기

        pred = np.zeros((height, width), dtype=np.uint8)  # 최종 결과 저장용

        # ✅ 슬라이딩 윈도우 적용
        for x in range(0 + OFFSET, width - OFFSET, CROP_SIZE):
            for y in range(0, height, CROP_SIZE):
                box = (x, y,
                        x + CROP_SIZE if x + CROP_SIZE < width else width,
                        y + CROP_SIZE if y + CROP_SIZE < height else height)
                output = model(input_tensor[:, :, y:box[3], x:box[2]])
                pred[y:box[3], x:box[2]] = np.argmax(output[0].detach().cpu().clone().numpy(), axis=0)

        # ✅ JSON 및 외곽선 이미지 저장
        pollution_contours = extract_contour_coordinates((pred == 1).astype(np.uint8), "Pollution")
        damaged_contours = extract_contour_coordinates((pred == 2).astype(np.uint8), "Damaged")
        battery_outline_contours = extract_contour_coordinates((pred == 3).astype(np.uint8), "Battery_Outline")

        # ✅ JSON 파일 저장
        json_path = os.path.join(result_folder, f"{os.path.basename(image_path).split('.')[0]}_pr.json")
        save_pr_json(json_path, pollution_contours, damaged_contours, battery_outline_contours)

        result = {"json_path": json_path}
        # result = {"json_path": json_path, "outline_image_path": outline_image_path}

        return result

    except Exception as e:
        print(f"❌ 이미지 처리 중 오류 발생: {image_path}, {e}")
