import torch
from ai.ai_model.model_loader import get_model
from ai.dataloaders.datasets.simple import SimpleSegmentation

model, device = get_model()

def predict_images(image_list):
    """FastAPI 요청에서 받은 이미지를 추론하는 함수"""
    dataset = SimpleSegmentation(images=image_list)
    preds_list = []

    with torch.no_grad():
        for sample in dataset:
            image = sample["image"].unsqueeze(0).to(device)
            output = model(image)
            pred = torch.argmax(output, dim=1).cpu().numpy()
            preds_list.append(pred)

    return preds_list  # ✅ metric 계산 없이 추론 결과만 반환
