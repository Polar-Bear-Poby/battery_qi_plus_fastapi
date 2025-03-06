import torch
from ai.ai_model.deeplab import DeepLab
from ai.mypath import Path  # 모델 경로 관리

# ✅ 모델 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
model_path = Path.get_model_weights()
model = DeepLab(backbone="drn", output_stride=8, num_classes=4).to(device)

# ✅ 가중치 불러오기
checkpoint = torch.load(model_path, map_location=device)
if "state_dict" in checkpoint:
    state_dict = checkpoint["state_dict"]
else:
    state_dict = checkpoint

model.load_state_dict(state_dict, strict=False)
model.eval()

def get_model():
    """ FastAPI에서 모델을 사용할 수 있도록 반환하는 함수 """
    return model, device
