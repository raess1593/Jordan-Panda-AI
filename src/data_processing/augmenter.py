from torchvision import transforms
from PIL import Image
from pathlib import Path

# Use this module to have more data samples in processed imgs
class ImgAumenter:
    def __init__(self):
        self.transform_pipeline = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.RandomPerspective(distortion_scale=0.2, p=0.5),
            transforms.RandomResizedCrop(size=(224, 224), scale=(0.7, 1.0))
        ])
    
    def multiply(self, input_path, output_path, multiplier=5):
        input_path.mkdir(parents=True, exist_ok=True)
        output_path.mkdir(parents=True, exist_ok=True)
        counter = 0
        for img_path in input_path.iterdir():
            if img_path.suffix.lower() in [".jpg", ".png", ".jpeg"]:
                img = Image.open(img_path).convert("RGBA").convert("RGB")

                for i in range(multiplier):
                    augmented_img = self.transform_pipeline(img)
                    new_name = f"aug_{i}_{img_path.stem}.jpg"
                    augmented_img.save(output_path / new_name)
                counter += multiplier
                print(f"AUGMENTED: {counter}")
    
def run_augmentation():
    root_path = Path(__file__).parent.parent.parent
    augmenter = ImgAumenter()
    augmenter.multiply(
        root_path / "data" / "raw" / "jordan_panda",
        root_path / "data" / "processed" / "jordan_panda", 
        multiplier=5
        )
    augmenter.multiply(
        root_path / "data" / "raw" / "not_jordan_panda",
        root_path / "data" / "processed" / "not_jordan_panda", 
        multiplier=5
        )

if __name__ == "__main__":
    run_augmentation()