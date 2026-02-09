from torchvision import transforms
from PIL import Image
from pathlib import Path

# Use this module to have more data samples in processed imgs
class ImgAumenter:
    def __init__(self):
        self.transform_pipeline = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomGrayscale(0.3),
            transforms.RandomRotation(degrees=20),
            transforms.ColorJitter(brightness=0.2),
            transforms.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0))
        ])
    
    def multiply(self, input_path, output_path, multiplier=10):
        for img_path in input_path.iterdir():
            if img_path.suffix.lower() in [".jpg", ".png", ".jpeg"]:
                img = Image.open(img_path).convert("RGB")

                for i in range(multiplier):
                    augmented_img = self.transform_pipeline(img)
                    new_name = f"aug_{i}_{img_path.stem}.jpg"
                    augmented_img.save(output_path / new_name)
    
def run_augmentation():
    base_dir = Path(__file__).parent.parent.parent
    augmenter = ImgAumenter()
    augmenter.multiply(
        base_dir / "data" / "raw" / "jordan_panda",
        base_dir / "data" / "processed" / "jordan_panda", 
        multiplier=20
        )
    augmenter.multiply(
        base_dir / "data" / "raw" / "not_jordan_panda",
        base_dir / "data" / "processed" / "not_jordan_panda", 
        multiplier=20
        )

if __name__ == "__main__":
    run_augmentation()