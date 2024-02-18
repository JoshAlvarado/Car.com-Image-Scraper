import torch
from PIL import Image
import os
import shutil  # For copying files

def main():
    # Load the model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()

    source_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205"
    target_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\Debugging"

    # Ensure target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    image_files = os.listdir(source_dir)
    matches_found = 0

    for img_file in image_files:
        if matches_found >= 25:
            break  # Stop after finding 25 matches

        img_path = os.path.join(source_dir, img_file)
        img = Image.open(img_path).convert("RGB")

        # Perform detection
        results = model(img, size=640)

        for *box, conf, cls in results.xyxy[0]:
            # Check for car detections with confidence between 0.60 and 0.65
            if results.names[int(cls)] == 'car' and 0.60 <= conf <= 0.65:
                # Copy this image to the target directory
                shutil.copy(img_path, os.path.join(target_dir, img_file))
                
                matches_found += 1
                break  # Move to the next image after finding the first car match

if __name__ == "__main__":
    main()
