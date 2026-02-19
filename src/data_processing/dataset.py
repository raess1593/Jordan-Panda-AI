from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

class JordanPandaDataset(Dataset):
    def __init__(self, root_dir:Path, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.image_labels = []

        for label, category in enumerate(["not_jordan_panda", "jordan_panda"]):
            current_dir = self.root_dir / category
            current_dir.mkdir(parents=True, exist_ok=True)
            for img_name in current_dir.iterdir():
                self.image_paths.append(current_dir / img_name)
                self.image_labels.append(label)

    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, index):
        img_path = self.image_paths[index]
        image = Image.open(img_path).convert("RGB")
        label = self.image_labels[index]

        if self.transform:
            image = self.transform(image)

        return image, label