import torch
from PIL import Image
import requests
from yolov5 import YOLOv5

def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(requests.get(url, stream=True).raw)

def main():
    # Load model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = YOLOv5("yolov5s", device=device)  # yolov5s is the smallest model

    # Load image
    img_url = "YOUR_IMAGE_URL_HERE"  # Replace with your image URL
    img = load_image_from_url(img_url)

    # Inference
    results = model.predict(img)

    # Results
    results.show()  # or .save(), .print(), etc.

    # Filter for cars and print results
    for result in results.xyxy[0]:
        # result format: xmin, ymin, xmax, ymax, confidence, class, name
        if result[-1] == "car":
            print(f"Car detected: {result[:-2].tolist()}")

if __name__ == "__main__":
    main()
