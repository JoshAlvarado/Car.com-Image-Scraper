import torch
from PIL import Image, UnidentifiedImageError, ImageFile
import os
import imagehash
import time

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Function to load an image from a file
def load_image_from_file(file_path):
    try:
        img = Image.open(file_path)
        img.load()  # Ensure the image is fully loaded
        return img, img.size
    except (UnidentifiedImageError, OSError) as e:
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
def process_image(img_path, model, hashes, hash_func, conf_threshold, bbox_ratio_min, bbox_ratio_max):
    img, (width, height) = load_image_from_file(img_path)

    # Skip processing if the image couldn't be opened
    if img is None:
        return False, "unloadable"

    # Check for duplicates
    if is_duplicate(img, hashes, hash_func):
        os.remove(img_path)
        return False, "duplicate"

    # Perform detection
    results = model(img)

    largest_bbox_area = 0
    largest_conf = 0

    for *box, conf, cls in results.xyxy[0]:
        if results.names[int(cls)] == 'car':
            x1, y1, x2, y2 = [int(coord.item()) for coord in box]
            bbox_area = (x2 - x1) * (y2 - y1)

            if bbox_area > largest_bbox_area:
                largest_bbox_area = bbox_area
                largest_conf = conf

    if largest_bbox_area > 0:
        img_area = width * height
        bbox_ratio = largest_bbox_area / img_area

        if largest_conf >= conf_threshold and bbox_ratio_min <= bbox_ratio <= bbox_ratio_max:
            return True, "kept"  # Keep the image

    # If the largest bounding box does not meet the criteria, delete the image file
    os.remove(img_path)
    return False, "not_criteria"

def main():
    start_time = time.time()

    model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()

    folder_path = r"l34"
    hashes = set()
    hash_func = imagehash.average_hash

    # Parameters from the hyperparameter optimization
    conf_threshold = 0.63  # Rounded to two decimal places
    bbox_ratio_min = 0.21  # Rounded to two decimal places
    bbox_ratio_max = 0.90  # Rounded to two decimal places

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_images = len(image_files)
    print(f"Total number of images in the folder: {total_images}")

    processed_images = 0
    kept_images = 0
    duplicate_images = 0
    unloadable_images = 0
    not_criteria_images = 0

    for filename in image_files:
        img_path = os.path.join(folder_path, filename)
        result, reason = process_image(img_path, model, hashes, hash_func, conf_threshold, bbox_ratio_min, bbox_ratio_max)
        processed_images += 1

        if reason == "kept":
            kept_images += 1
        elif reason == "duplicate":
            duplicate_images += 1
        elif reason == "unloadable":
            unloadable_images += 1
        elif reason == "not_criteria":
            not_criteria_images += 1

        if processed_images % 1000 == 0:
            percentage_done = (processed_images / total_images) * 100
            print(f"{percentage_done:.2f}% done. {processed_images} out of {total_images} images processed.")

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Total images processed: {processed_images}")
    print(f"Images kept: {kept_images}")
    print(f"Duplicate images deleted: {duplicate_images}")
    print(f"Unloadable images deleted: {unloadable_images}")
    print(f"Images deleted for not meeting criteria: {not_criteria_images}")

if __name__ == "__main__":
    main()
