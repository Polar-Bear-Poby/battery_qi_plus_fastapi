# import os
# import time
# import requests
# import shutil
# import asyncio
# import httpx
# from config.settings import FOLDER_A, FOLDER_B
#
# FASTAPI_URL = "http://127.0.0.1:8000"
#
# # ✅ 배터리 셀 ID별 원판 회전 각도를 저장하는 딕셔너리
# collected_images = {}
#
# # ✅ 감시할 필수 원판 회전 각도 목록 (배터리 셀을 0°, 90°, 180°, 270° 회전하며 촬영)
# REQUIRED_ROTATION_ANGLES = {0, 90, 180, 270}
#
# # ✅ 감시 중인 배터리 ID 리스트 (Set 자료구조 사용 → 중복 방지)
# battery_watch_list = set()
#
# async def watch_folder_A():
#     """
#     📌 폴더 A 감시하여 배터리 셀 ID별 PNG 파일 추적 및 AI 추론 요청.
#     📌 0°, 90°, 180°, 270° 촬영 완료 시 AI 추론 실행 및 `battery_watch_list`에 추가.
#     📌 폴더 A 내 `{배터리_id}` 폴더를 생성하고 촬영된 이미지를 이동하도록 수정.
#     """
#     print(f"🚀 [폴더 감시] 폴더 A 감시 시작!")
#
#     while True:
#         for file_name in os.listdir(FOLDER_A):
#             file_path = os.path.join(FOLDER_A, file_name)
#
#             if os.path.isfile(file_path) and file_name.endswith(".png"):
#                 parts = file_name.split("_")
#
#                 try:
#                     battery_id = parts[3]  # 배터리 셀 ID
#                     rotation_angle = int(parts[6].replace(".png", ""))  # 원판 회전 각도
#                 except ValueError:
#                     continue
#
#                 # ✅ 배터리 ID별 원판 회전 각도를 저장
#                 if battery_id not in collected_images:
#                     collected_images[battery_id] = set()
#
#                 collected_images[battery_id].add(rotation_angle)
#
#                 # ✅ 배터리별 폴더 생성
#                 battery_folder = os.path.join(FOLDER_A, str(battery_id))
#                 if not os.path.exists(battery_folder):
#                     os.makedirs(battery_folder)
#                     print(f"✅ [폴더 생성] 배터리 {battery_id} 폴더 생성 완료: {battery_folder}")
#
#                 # ✅ 기존 촬영된 이미지를 배터리 ID 폴더로 이동
#                 new_path = os.path.join(battery_folder, file_name)
#                 if not os.path.exists(new_path):
#                     shutil.move(file_path, new_path)
#                     print(f"✅ [이미지 이동] {file_name} → {battery_folder}")
#
#                 print(f"📌 [디버그] collected_images: {collected_images}")
#
#                 # ✅ 모든 필수 원판 회전 각도 감지 시 AI 추론 요청 실행
#                 if REQUIRED_ROTATION_ANGLES.issubset(collected_images[battery_id]):
#                     print(f"🚀 배터리 {battery_id} 모든 필수 원판 회전 완료 → AI 추론 요청 실행")
#
#                     # ✅ `result/` 하위 폴더 생성
#                     result_folder = os.path.join(battery_folder, "result")
#                     if not os.path.exists(result_folder):
#                         os.makedirs(result_folder)
#                         print(f"✅ [폴더 생성] 배터리 {battery_id}/result 폴더 생성 완료")
#
#                     # ✅ AI 추론 실행
#                     await request_prediction(battery_id)
#
#                     # ✅ 배터리 감시 리스트에 추가
#                     battery_watch_list.add(battery_id)
#
#         await asyncio.sleep(2)  # 2초마다 폴더 확인
#
#
# async def watch_folder_B_result():
#     """
#     📌 `battery_watch_list`에 있는 배터리 셀 ID의 `result` 폴더 감시 후 업로드 실행.
#     """
#     print("🚀 [폴더 감시] 폴더 B 결과 폴더 감시 시작!")
#
#     while True:
#         for battery_id in list(battery_watch_list):  # Set을 리스트로 변환하여 반복
#             result_folder = os.path.join(FOLDER_B, battery_id, "result")
#
#             if not os.path.exists(result_folder):
#                 continue
#
#             # ✅ JSON 파일 개수 확인
#             result_files = [f for f in os.listdir(result_folder) if f.endswith(".json")]
#
#             if len(result_files) >= 8:  # JSON 8개 이상이면 업로드 요청
#                 print(f"🚀 배터리 {battery_id} 결과 파일 감지 → 업로드 요청 실행")
#
#                 # ✅ 업로드 요청 실행
#                 await request_upload(battery_id)
#
#                 # ✅ 배터리 감시 리스트에서 제거
#                 battery_watch_list.remove(battery_id)
#
#         await asyncio.sleep(5)  # 5초마다 폴더 확인
#
#
# async def request_prediction(battery_id):
#     """
#     📌 AI 추론 요청 (predict.py 호출)
#     """
#     print(f"🚀 AI 추론 요청 실행: 배터리 {battery_id}")
#     url = f"{FASTAPI_URL}/predict/{battery_id}"
#
#     async with httpx.AsyncClient() as client:
#         await client.post(url, json={})
#
#
# async def request_upload(battery_id):
#     """
#     📌 AI 결과 업로드 요청 (upload.py 호출)
#     """
#     print(f"🚀 업로드 요청 실행: 배터리 {battery_id}")
#     url = f"{FASTAPI_URL}/upload/{battery_id}"
#
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, json={})
#
#     if response.status_code == 200:
#         print(f"✅ 배터리 {battery_id} 결과 업로드 성공")
#     else:
#         print(f"❌ 배터리 {battery_id} 결과 업로드 실패: {response.text}")


import os
import time
import requests
import shutil
import asyncio
import httpx
from config.settings import FOLDER_A, FOLDER_B
from concurrent.futures import ThreadPoolExecutor

FASTAPI_URL = "http://127.0.0.1:8000"

# ✅ 배터리 셀 ID별 원판 회전 각도를 저장하는 딕셔너리
collected_images = {}

# ✅ 감시할 필수 원판 회전 각도 목록 (배터리 셀을 0°, 90°, 180°, 270° 회전하며 촬영)
REQUIRED_ROTATION_ANGLES = {0, 90, 180, 270}

# ✅ 배터리 셀 ID 처리 대기열 (FIFO 큐 → AI 추론 요청용)
battery_queue = asyncio.Queue()

# ✅ 감시할 배터리 셀 ID 대기열 (FIFO 큐 → `result` 폴더 감시용)
battery_watch_queue = asyncio.Queue()

# ✅ ThreadPoolExecutor (폴더 감시 비동기 실행)
executor = ThreadPoolExecutor(max_workers=2)


async def print_queue_status():
    """
    📌 각 큐의 상태를 주기적으로 출력하는 함수
    """
    while True:
        battery_queue_list = list(battery_queue._queue)  # asyncio.Queue 내부 리스트 접근
        battery_watch_queue_list = list(battery_watch_queue._queue)

        print(f"🔄 [디버그] battery_queue 상태: {battery_queue_list}")
        print(f"🔄 [디버그] battery_watch_queue 상태: {battery_watch_queue_list}")

        await asyncio.sleep(5)  # 5초마다 출력


async def watch_folder_A():
    """
    📌 폴더 A를 감시하여 배터리 셀 ID별 PNG 파일을 추적
    📌 배터리 셀을 원판 위에 올리고 0°, 90°, 180°, 270°로 회전하며 촬영된 이미지가 수집되었는지 확인
    📌 모든 원판 회전 각도 이미지가 수집되면 AI 추론 요청 실행
    📌 AI 추론 요청과 동시에 감시할 배터리 셀 ID를 `battery_watch_queue`에 추가
    """
    print(f"🚀 [폴더 감시] 폴더 A 감시 시작!")

    while True:
        for file_name in os.listdir(FOLDER_A):
            file_path = os.path.join(FOLDER_A, file_name)

            # ✅ PNG 파일인지 확인
            if os.path.isfile(file_path) and file_name.endswith(".png"):
                parts = file_name.split("_")

                try:
                    battery_id = parts[3]  # 배터리 셀 ID
                    rotation_angle = int(parts[6].replace(".png", ""))  # 원판 회전 각도
                except ValueError:
                    continue

                # ✅ 배터리 ID별 원판 회전 각도를 저장
                if battery_id not in collected_images:
                    collected_images[battery_id] = set()

                collected_images[battery_id].add(rotation_angle)

                print(f"📌 [디버그] collected_images: {collected_images}")

                # ✅ 필수 원판 회전 각도가 모두 감지되었는지 확인
                if REQUIRED_ROTATION_ANGLES.issubset(collected_images[battery_id]):
                    print(f"🚀 배터리 {battery_id} 모든 필수 원판 회전 완료 → AI 추론 요청 준비")

                    battery_folder = os.path.join(FOLDER_A, str(battery_id))
                    if not os.path.exists(battery_folder):
                        os.makedirs(battery_folder)
                        print(f"✅ [폴더 생성] 배터리 {battery_id} 폴더 생성 완료: {battery_folder}")

                    # ✅ 기존 이미지를 배터리 ID 폴더로 이동
                    for file_name in os.listdir(FOLDER_A):
                        if file_name.startswith(f"RGB_cell_cylindrical_{battery_id}_"):
                            old_path = os.path.join(FOLDER_A, file_name)
                            new_path = os.path.join(battery_folder, file_name)

                            shutil.move(old_path, new_path)  # 이미지 이동
                            print(f"✅ [이미지 이동] {file_name} → {battery_folder}")

                    # ✅ `result/` 하위 폴더 생성
                    result_folder = os.path.join(battery_folder, "result")
                    if not os.path.exists(result_folder):
                        os.makedirs(result_folder)
                        print(f"✅ [폴더 생성] 배터리 {battery_id}/result 폴더 생성 완료")

                    # ✅ AI 추론 대기열 추가 (FIFO 큐)
                    await battery_queue.put(battery_id)

                    # ✅ AI 추론 요청 실행 (백그라운드 실행)
                    asyncio.create_task(request_prediction(battery_id))

                    # ✅ `result` 폴더 감시 대기열 추가
                    await battery_watch_queue.put(battery_id)

        await asyncio.sleep(2)  # 2초마다 폴더 확인


async def watch_folder_B_result():
    """
    📌 `battery_watch_queue`에서 감시할 배터리 셀 ID를 가져와 `result` 폴더 감시
    📌 배터리 셀 ID별 `result` 폴더가 생성되고 JSON 8개 & 외곽선 이미지 8개가 저장되었는지 확인
    📌 결과 업로드 요청 후 `battery_watch_queue`에서 제거
    """
    print("🚀 [폴더 감시] 폴더 B 결과 폴더 감시 시작!")
    print(f"Folder B: {FOLDER_B}")

    while True:
        for battery_id in list(battery_watch_queue._queue):
            result_folder = os.path.join(FOLDER_B, battery_id, "result")

            # ✅ `result` 폴더가 존재하는 경우만 감시
            if not os.path.exists(result_folder):
                continue

            # ✅ 결과 JSON & 외곽선 이미지 개수 확인
            result_files = [f for f in os.listdir(result_folder) if f.endswith((".json"))]

            if len(result_files) >= 8:  # JSON 8개 + 이미지 8개
                print(f"🚀 배터리 {battery_id} 결과 파일 감지 → 업로드 요청 실행")

                # ✅ 업로드 요청 실행
                await request_upload(battery_id)

                # ✅ 업로드 완료 후 감시 목록에서 제거
                await battery_watch_queue.get()
                battery_watch_queue.task_done()

        await asyncio.sleep(5)  # 5초마다 폴더 확인


async def request_prediction(battery_id):
    """
    📌 AI 추론 요청 (predict.py 호출)
    📌 감시할 배터리 ID를 `battery_watch_queue`에 추가
    """
    print("request_prediction 실행!")
    print(f"battery_id: {battery_id}")
    url = f"{FASTAPI_URL}/predict/{battery_id}"
    print(f"url: {url}")

    async with httpx.AsyncClient() as client:
        await client.post(url, json={})

async def request_upload(battery_id):
    """
    📌 AI 결과 업로드 요청 (upload.py 호출)
    """
    url = f"{FASTAPI_URL}/upload/{battery_id}"
    response = requests.post(url, json={})

    if response.status_code == 200:
        print(f"✅ 배터리 {battery_id} 결과 업로드 요청 성공")
    else:
        print(f"❌ 배터리 {battery_id} 결과 업로드 요청 실패: {response.text}")
