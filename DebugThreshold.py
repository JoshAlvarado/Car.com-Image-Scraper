import torch
from PIL import Image, UnidentifiedImageError
import os
import shutil  # For copying files
import random  # For randomizing image selection

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
    random.shuffle(image_files)  # Randomize the order of files
    matches_found = 0

    for img_file in image_files:
        if matches_found >= 100:
            break  # Stop after finding 25 matches

        img_path = os.path.join(source_dir, img_file)
        try:
            img = Image.open(img_path).convert("RGB")
        except UnidentifiedImageError:
            print(f"Skipping file due to error opening: {img_file}")
            continue  # Skip this file and continue with the next one

        # Perform detection
        results = model(img, size=640)

        for *box, conf, cls in results.xyxy[0]:
            if results.names[int(cls)] == 'car':
                x1, y1, x2, y2 = box
                bbox_area = (x2 - x1) * (y2 - y1)
                img_area = img.width * img.height
                bbox_ratio = bbox_area / img_area

                # Check for car detections with confidence between 0.60 and 0.65 and bbox area over 30% of the image
                #if 0.60 <= conf <= 0.65 and bbox_ratio >= 0.3:
                if 0.60 <= conf and 0.20 <= bbox_ratio <= 0.30:
                    # Copy this image to the target directory
                    shutil.copy(img_path, os.path.join(target_dir, img_file))
                    
                    matches_found += 1
                    break  # Move to the next image after finding the first car match

if __name__ == "__main__":
    main()
