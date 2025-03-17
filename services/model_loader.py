import torch
import os
from ai.ai_model.deeplab import DeepLab

# ✅ 모델 캐싱 (한 번만 로드)
_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_model():
    """
    📌 AI 모델을 한 번만 로드하고, 이후에는 캐싱된 모델을 사용
    """
    global _model

    if _model is None:
        model_path = r"D:\2025_1\battery_qi_fastapi\ai\weights\battery_rgb.pt"  # ✅ 가중치 파일 경로 지정
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"❌ 모델 가중치 파일이 존재하지 않습니다: {model_path}")

        print("🚀 모델 로드 중...")
        _model = DeepLab(num_classes=4, backbone="drn", sync_bn=False, freeze_bn=False)
        checkpoint = torch.load(model_path, map_location=_device, weights_only=False)  # ✅ CPU 또는 GPU 환경 자동 적용
        _model.load_state_dict(checkpoint['state_dict'])
        _model.to(_device)
        _model.eval()
        print("✅ 모델 로드 완료!")

    return _model

def unload_model():
    """
    📌 AI 모델 언로드 (메모리에서 삭제)
    - C#에서 shutdown 명령이 들어왔을 때 사용 가능
    """
    global _model

    if _model is not None:
        print("🔄 모델 언로드 중...")
        del _model
        _model = None
        torch.cuda.empty_cache()  # ✅ GPU 캐시 정리 (GPU 사용 시)
        print("✅ 모델 언로드 완료!")
