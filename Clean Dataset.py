import torch
from PIL import Image, UnidentifiedImageError
import os
import imagehash

# Function to load an image from a file
def load_image_from_file(file_path):
    try:
        img = Image.open(file_path)
        return img, img.size
    except UnidentifiedImageError:
        print(f"Error opening image file {file_path}. Deleting file.")
        os.remove(file_path)
        return None, (0, 0)

# Function to check if an image is a duplicate
def is_duplicate(img, hashes, hash_func, threshold=5):
    img_hash = hash_func(img)
    for stored_hash in hashes:
        if abs(img_hash - stored_hash) <= threshold:
            return True
    hashes.add(img_hash)
    return False

# Process each image for car detection and duplicate removal
def process_image(img_path, model, hashes, hash_func, bbox_area_threshold=0.3, confidence_threshold=0.65):
    img, (width, height) = load_image_from_file(img_path)

    # Skip processing if the image couldn't be opened
    if img is None:
        return

    # Check for duplicates
    if is_duplicate(img, hashes, hash_func):
        print(f"Duplicate image detected: {os.path.basename(img_path)}. Deleting image.")
        os.remove(img_path)
        return

    # Perform detection
    results = model(img)

    large_car_detected = False
    for *box, conf, cls in results.xyxy[0]:
        if results.names[int(cls)] == 'car' and conf > confidence_threshold:
            x1, y1, x2, y2 = box
            bbox_area = (x2 - x1) * (y2 - y1)
            img_area = width * height
            bbox_ratio = bbox_area / img_area

            if bbox_ratio > bbox_area_threshold:
                print(f"Large car detected in {os.path.basename(img_path)} with confidence {conf}")
                large_car_detected = True
                break

    # If a large car is not detected, delete the image file
    if not large_car_detected:
        print(f"No large car detected in {os.path.basename(img_path)}. Deleting image.")
        os.remove(img_path)

def main():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()

    folder_path = r"c:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205"
    hashes = set()
    hash_func = imagehash.average_hash

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            process_image(img_path, model, hashes, hash_func)

if __name__ == "__main__":
    main()
