from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torchvision import transforms

from model import JordanPandaModel
from data_processing.dataset import JordanPandaDataset 

def main():
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    root_path = Path(__file__).parent.parent / "data" / "processed"
    full_dataset = JordanPandaDataset(root_dir=root_path, transform=transform)
    
    train_size = int(len(full_dataset)*0.8)
    test_size = len(full_dataset) - train_size

    train_dataset, test_dataset = random_split(dataset=full_dataset, lengths=[train_size, test_size])
    
    train_loader = DataLoader(dataset=train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(dataset=test_dataset, batch_size=16, shuffle=False)

    model = JordanPandaModel()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(params=model.parameters(), lr=0.001)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    model.train()
    epochs = 20
    losses = []
    for e in range(epochs):
        running_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()

            results = model(images)
            loss = criterion(results, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        
        losses.append(running_loss / len(train_loader))
        print(f"Epoch {e+1}/{epochs}\n\tLoss: {running_loss / len(train_loader):.4f}")

    model.eval()
    with torch.no_grad():
        successes = 0
        total = 0
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device) 

            results = model(images)
            indexes = results.argmax(dim=1)

            successes += (indexes == labels).sum().item()
            total += len(labels)
        
        accuracy = successes / total * 100
        print(f"--> Accuracy: {accuracy}%")
            

if __name__ == "__main__":
    main()