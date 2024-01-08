import torch
from PIL import Image
import os

# Function to load an image from a file
def load_image_from_file(file_path):
    img = Image.open(file_path)
    return img, img.size

def process_image(img_path, model, bbox_area_threshold=0.3, confidence_threshold=0.65):
    # Load image and get its size
    img, (width, height) = load_image_from_file(img_path)

    # Perform detection
    results = model(img)

    # Iterate through detection results
    for *box, conf, cls in results.xyxy[0]:
        if results.names[int(cls)] == 'car' and conf > confidence_threshold:
            # Calculate the area of the bounding box
            x1, y1, x2, y2 = box
            bbox_area = (x2 - x1) * (y2 - y1)
            img_area = width * height
            bbox_ratio = bbox_area / img_area

            # Check if the bounding box is large enough
            if bbox_ratio > bbox_area_threshold:
                print(f"Large car detected in {os.path.basename(img_path)} with confidence {conf}")
                results.show()
                break

def main():
    # Load the model from the official YOLOv5 repository
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()

    # Folder path
    folder_path = r"c:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205"

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            process_image(img_path, model)

if __name__ == "__main__":
    main()
