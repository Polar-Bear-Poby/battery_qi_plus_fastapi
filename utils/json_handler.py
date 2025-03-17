import json
import itertools
import os

def save_pr_json(output_json_path, pollution_contours, damaged_contours, battery_outline_contours):
    """
    📌 AI 추론 결과 JSON 저장 (딥러닝 프로젝트의 JSON 형식 반영)
    - `output_json_path`: 저장할 JSON 파일 경로
    - `pollution_contours`: 오염 외곽선
    - `damaged_contours`: 손상 외곽선
    - `battery_outline_contours`: 배터리 외곽선
    """

    # ✅ 초기 JSON 구조 설정
    output_json_data = {
        "defects": [],
        "image_info": {
            "is_normal": True  # 기본값 (결함이 감지되면 False로 변경)
        },
        "battery_outline": []  # 배터리 외곽선은 별도로 저장
    }

    # ✅ `defects` 리스트에 Pollution 및 Damaged 추가 (좌표를 1D 리스트로 변환)
    output_json_data["defects"].extend([
        {
            "id": 2,
            "name": "Pollution",
            "points": list(itertools.chain.from_iterable(instance["contour"]))
        }
        for instance in pollution_contours
    ] + [
        {
            "id": 1,
            "name": "Damaged",
            "points": list(itertools.chain.from_iterable(instance["contour"]))
        }
        for instance in damaged_contours
    ])

    # ✅ `battery_outline` 저장 (2D 리스트 → 1D 리스트 변환 적용)
    output_json_data["battery_outline"] = list(
        itertools.chain.from_iterable(itertools.chain.from_iterable(instance["contour"] for instance in battery_outline_contours))
    )

    # ✅ `is_normal` 업데이트 (defects가 하나라도 존재하면 False, 없으면 True)
    output_json_data["image_info"]["is_normal"] = len(output_json_data["defects"]) == 0

    # ✅ JSON 저장
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output_json_data, f, indent=4, ensure_ascii=False)

    print(f"[저장 완료] AI 추론 결과 JSON → {output_json_path}")
