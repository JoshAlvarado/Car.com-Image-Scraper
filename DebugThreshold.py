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
    target_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\debuggingParameterslowconf"
    cleaned_dir = os.path.join(target_dir, 'cleaned')
    discarded_dir = os.path.join(target_dir, 'discarded')

    # Ensure target and subdirectories exist
    if not os.path.exists(cleaned_dir):
        os.makedirs(cleaned_dir)
    if not os.path.exists(discarded_dir):
        os.makedirs(discarded_dir)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)    

    image_files = os.listdir(source_dir)
    random.shuffle(image_files)  # Randomize the order of files
    matches_found = 0

    for img_file in image_files:
        if matches_found >= 250:
            break  # Stop after finding 100 matches

        img_path = os.path.join(source_dir, img_file)
        try:
            img = Image.open(img_path).convert("RGB")
        except UnidentifiedImageError:
            print(f"Skipping file due to error opening: {img_file}")
            continue  # Skip this file and continue with the next one

        # Perform detection
        results = model(img, size=640)

        # Initialize variable to track the largest box
        largest_bbox_area = 0
        largest_conf = 0

        for *box, conf, cls in results.xyxy[0]:
            if results.names[int(cls)] == 'car':
                x1, y1, x2, y2 = box
                bbox_area = (x2 - x1) * (y2 - y1)
                
                if bbox_area > largest_bbox_area:
                    largest_bbox_area = bbox_area
                    largest_conf = conf

        if largest_bbox_area > 0:
            img_area = img.width * img.height
            bbox_ratio = largest_bbox_area / img_area

            # Debug print statements to check the values
            # print(f"Processing file: {img_file}")
            # print(f"Largest Confidence: {largest_conf}, BBox ratio: {bbox_ratio}")
            # print(f"Largest BBox area: {largest_bbox_area}, Image area: {img_area}")

            # Check for car detections with confidence and bbox area criteria
            if largest_conf >= 0.30 and .15 <= bbox_ratio <= 0.87:
                # Copy this image to the cleaned directory
                shutil.copy(img_path, os.path.join(cleaned_dir, img_file))
                matches_found += 1
            else:
                # Copy this image to the discarded directory
                shutil.copy(img_path, os.path.join(discarded_dir, img_file))

if __name__ == "__main__":
    main()
