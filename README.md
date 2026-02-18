# 🐼 Panda-Scout AI: End-to-End Sneaker Classifier

**Panda-Scout AI** is a professional-grade Data Engineering and Computer Vision project designed to automate the detection of **Nike Jordan 1 "Panda"** sneakers in secondary markets. This project serves as a comprehensive proof-of-concept for high-scale data acquisition and deep learning inference.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)

## 🚀 Overview
The system automates the entire machine learning lifecycle:
1.  **Data Ingestion:** Automated scraping of Nike (Official) and Wallapop (Market) using anti-bot bypass techniques.
2.  **Preprocessing:** Image augmentation to diversify training samples and prevent early-stage overfitting.
3.  **Model Training:** A custom Convolutional Neural Network (CNN) built with PyTorch, optimized through iterative evaluation.
4.  **Inference:** A production-ready script to classify local images with confidence scoring.

## 🛠️ Tech Stack
* **Automation:** Selenium & `undetected-chromedriver` for advanced web scraping.
* **AI/ML:** PyTorch, Torchvision (Transforms), and PIL.
* **Data Handling:** Pandas for metadata management and Pathlib for robust file system navigation.
* **Environment:** Python 3.10+.

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Panda-Scout-AI.git](https://github.com/YOUR_USERNAME/Panda-Scout-AI.git)
   cd Panda-Scout-AI
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
3. **Install dependencies:**
   ```bash
   pip install torch torchvision pillow selenium undetected-chromedriver webdriver-manager pandas requests

## 🎯 Educational Objectives & Results

This project was developed as part of a Data Engineering specialization, focusing on mastering data pipelines and real-world AI challenges.

*   **Final Accuracy:** 80.26% on the validation set after 10 epochs.
*   **Optimization:** Identified a significant improvement (from 57% to 80%) by balancing real-world market data with high-quality catalog images.
*   **Lessons Learned:** Successfully navigated the "Overfitting" phase, identifying that extremely low training loss ($0.0091$) requires a more diverse negative-sample dataset to maintain high real-world precision.

## ⚠️ Industrial Scalability

To transition this PoC into a 99% accuracy commercial tool, the following enhancements are required:

1.  **Dataset Expansion:** Scaling from hundreds to thousands of unique samples.
2.  **Transfer Learning:** Implementing pre-trained architectures like ResNet50 or EfficientNet.
3.  **Hardware Acceleration:** Training on high-performance GPU clusters to support deeper architectures.

---
**Author:** raess1593 –  Data & AI Engineer Student
