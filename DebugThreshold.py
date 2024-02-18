import torch
from PIL import Image
import os
import torchvision.transforms as transforms

def load_image(file_path):
    try:
        with Image.open(file_path) as img:
            return img.convert('RGB')
    except Exception as e:
        print(f"Error loading image {file_path}: {e}")
        return None

def process_images(folder_path, debug_images_limit=25):
    # Load the model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()

    # Transformation for the input image
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    debug_images = []

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        img_path = os.path.join(folder_path, filename)
        img = load_image(img_path)
        if img is None:
            continue

        # Transform image and add batch dimension
        img_t = transform(img).unsqueeze(0).to(device)
        results = model(img_t)

        # Check the structure of results to ensure correct processing
        detections = results.xyxy[0]  # This should be the correct way to access detections

        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            bbox_area = (x2 - x1) * (y2 - y1)
            img_area = img.width * img.height
            bbox_ratio = bbox_area / img_area

            if 0.60 <= conf <= 0.65 and bbox_ratio > 0.3:
                debug_images.append(img_path)
                break

        if len(debug_images) >= debug_images_limit:
            break

    return debug_images

def main():
    folder_path = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205"
    debug_images = process_images(folder_path)
    print("Images meeting the criteria:")
    for img in debug_images:
        print(img)

if __name__ == "__main__":
    main()
