import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import os
from pathlib import Path
from model import JordanPandaModel

root_path = Path(__file__).parent.parent
i = 1
model_path = root_path / "models"
while i < 5:
    model_file = model_path / f"jordan_panda_model_{i}.pth"
    i += 1
    if model_file.exists():
        break
data_path = root_path / "data" / "evaluation"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = JordanPandaModel()
state_dict = torch.load(model_file, map_location=device)
model.load_state_dict(state_dict=state_dict)
model.eval()

transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

print(f"🚀 Starting evaluation: {data_path.name}\n" + "-"*30)

found_pandas = []
for img_path in data_path.iterdir():
    if img_path.suffix not in ['.jpg', '.jpeg', '.png']:
        continue

    img = Image.open(img_path).convert("RGBA").convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, dim=1)

        confidence_val = confidence.item()
        class_idx = predicted.item()

        if (class_idx == 1 and confidence_val >= 0.53) or (class_idx == 0 and confidence_val <= 0.6):
            print(f"✅ DETECTED: {img_path.name} | CONFIDENCE: {confidence_val*100:.2f}%")
            found_pandas.append(img_path.name)
        else:
            print(f"❌ Ignored: {img_path.name} | Probability: {probabilities[0][0].item()*100:.2f}%")

print("\n" + "-"*30)
print(f"📊 Summary: There have been detected {len(found_pandas)} Jordan Pandas with high confidence.")