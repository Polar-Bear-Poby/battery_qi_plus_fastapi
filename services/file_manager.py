import os
import json
import shutil
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.settings import FOLDER_B, FOLDER_C
from datetime import datetime

def analyze_results_store_and_move(battery_id: str, db: Session):
    """
    📌 검사 결과 JSON 8개를 분석하고 정상/불량 판별 후 DB 저장 및 파일 이동
    - `battery_id`: 검사한 배터리 셀 ID
    - `db`: SQLAlchemy 세션 객체 (Raw SQL 사용)
    """

    # ✅ 이동할 촬영각도 리스트 (A/B 포함)
    ANGLE_TARGETS = ["cameraAngle_A_0", "cameraAngle_A_90", "cameraAngle_A_180", "cameraAngle_A_270",
                     "cameraAngle_B_0", "cameraAngle_B_90", "cameraAngle_B_180", "cameraAngle_B_270"]

    result_folder = os.path.join(FOLDER_B, battery_id, "result")
    if not os.path.exists(result_folder):
        print(f"[⚠] 결과 JSON 폴더 없음: {result_folder}")
        return

    # ✅ 검사할 JSON 파일 수집
    json_files = [f for f in os.listdir(result_folder) if f.endswith("_pr.json")]

    # ✅ JSON 파일 개수가 8개(정상)인지 확인
    if len(json_files) != 8:
        print(f"[⚠] 배터리 {battery_id}: JSON 파일 개수 불일치 (총 {len(json_files)}개)")
        return

    # ✅ JSON 파일 검사 (배터리 정상/불량 판별)
    is_normal_all = True
    pollution_detected = False
    damage_detected = False

    for json_file in json_files:
        json_path = os.path.join(result_folder, json_file)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # ✅ `is_normal`이 하나라도 False면 배터리는 불량
            if not data.get("image_info", {}).get("is_normal", True):
                is_normal_all = False
                if data.get("defects"):
                    for defect in data["defects"]:
                        if defect["name"] == "Pollution":
                            pollution_detected = True
                        elif defect["name"] == "Damaged":
                            damage_detected = True

    # ✅ 최종 판정 결과
    fast_pollution_check = not is_normal_all and pollution_detected
    fast_damage_check = not is_normal_all and damage_detected

    # ✅ 검사 결과를 DB에 저장 (INSERT 또는 UPDATE)
    inspection_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ✅ 먼저 해당 배터리가 `InspectionResults`에 존재하는지 확인
    check_query = text("SELECT COUNT(*) FROM InspectionResults WHERE batteryId = :battery_id")
    result = db.execute(check_query, {"battery_id": battery_id}).scalar()

    if result == 0:
        # ✅ 존재하지 않으면 INSERT
        insert_query = text("""
            INSERT INTO InspectionResults (batteryId, inspectionDatetime, fastPollutionCheck, fastDamageCheck, InputMethod)
            VALUES (:battery_id, :inspection_datetime, :fast_pollution, :fast_damage, 'python')
        """)
        db.execute(insert_query, {
            "battery_id": battery_id,
            "inspection_datetime": inspection_datetime,
            "fast_pollution": fast_pollution_check,
            "fast_damage": fast_damage_check
        })
        print(f"✅ 배터리 {battery_id}: 검사 결과 삽입 완료")
    else:
        # ✅ 이미 존재하면 UPDATE
        update_query = text("""
            UPDATE InspectionResults
            SET inspectionDatetime = :inspection_datetime,
                fastPollutionCheck = :fast_pollution,
                fastDamageCheck = :fast_damage,
                InputMethod = 'python'
            WHERE batteryId = :battery_id
        """)
        db.execute(update_query, {
            "battery_id": battery_id,
            "inspection_datetime": inspection_datetime,
            "fast_pollution": fast_pollution_check,
            "fast_damage": fast_damage_check
        })
        print(f"✅ 배터리 {battery_id}: 검사 결과 업데이트 완료")

    db.commit()  # ✅ 변경 사항 커밋

    # ✅ 검사 결과 기반 파일 이동
    source_dir = os.path.join(FOLDER_B, battery_id)
    target_dir = os.path.join(FOLDER_C, battery_id)

    if not os.path.exists(source_dir):
        print(f"[⚠] 이동할 배터리 셀 데이터 없음: {source_dir}")
        return

    os.makedirs(target_dir, exist_ok=True)

    try:
        if is_normal_all:
            # ✅ 정상인 경우 전체 폴더 이동
            shutil.move(source_dir, target_dir)
            print(f"[✔] 배터리셀 {battery_id} 검사 데이터 전체 이동 완료: {target_dir}")
        else:
            # ✅ 불량인 경우 특정 파일만 이동
            for file_name in os.listdir(source_dir):
                # 촬영각도가 포함된 파일인지 확인 (A/B 포함)
                if any(angle in file_name for angle in ANGLE_TARGETS) or file_name.endswith("_pr.json"):
                    shutil.move(os.path.join(source_dir, file_name), os.path.join(target_dir, file_name))

            print(f"[✔] 배터리셀 {battery_id} 불량 데이터 선택적 이동 완료: {target_dir}")

    except Exception as e:
        print(f"[❌] 파일 이동 중 오류 발생: {e}")
