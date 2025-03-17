import cv2
import numpy as np
from PIL import Image, ImageDraw

def extract_contour_coordinates(mask, class_name):
    """
    📌 다중 클래스 객체를 저장하는 방식으로 변경
    - `binary_mask`: 특정 클래스의 바이너리 마스크 (numpy 배열)
    - `class_name`: 해당 클래스 이름 (예: "Pollution", "Damaged", "Battery_Outline")
    - 반환: [{"class": class_name, "contour": [[x1, y1], [x2, y2], ...]}] 형태의 리스트
    """
    """특정 클래스의 마스크에서 개별 객체의 외곽선 좌표를 추출 (최적화 버전)"""

    binary_mask = (mask > 0).astype(np.uint8)  # 변환 연산 최소화
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return [{
        "class": class_name,
        "contour": contour.reshape(-1, 2).tolist()
    } for contour in contours]

def add_pr_outline(image, pollution_contours, damaged_contours, battery_outline_contours):
    """
    📌 원본 이미지에 AI 모델이 검출한 외곽선 추가
    """
    draw = ImageDraw.Draw(image)

    # 오염 영역 (파란색)
    for contour in pollution_contours["Pollution"]:
        draw.polygon(contour, outline="blue")

    # 손상 영역 (빨간색)
    for contour in damaged_contours["Damaged"]:
        draw.polygon(contour, outline="red")

    # 배터리 외곽선 (초록색)
    for contour in battery_outline_contours["Battery_Outline"]:
        draw.polygon(contour, outline="green")

    return image
