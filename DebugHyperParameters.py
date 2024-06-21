import torch
from PIL import Image, UnidentifiedImageError
import os
import shutil
import optuna

def process_images(conf_threshold, bbox_ratio_threshold, good_dir, bad_dir):
    # Load the model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()

    def evaluate_folder(folder, expected_good):
        correct = 0
        total = 0

        for img_file in os.listdir(folder):
            img_path = os.path.join(folder, img_file)
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

                # Check for car detections with confidence and bbox area criteria
                if largest_conf >= conf_threshold and bbox_ratio >= bbox_ratio_threshold:
                    if expected_good:
                        correct += 1
                else:
                    if not expected_good:
                        correct += 1

            total += 1

        return correct, total

    good_correct, good_total = evaluate_folder(good_dir, True)
    bad_correct, bad_total = evaluate_folder(bad_dir, False)

    total_correct = good_correct + bad_correct
    total_images = good_total + bad_total

    accuracy = total_correct / total_images if total_images > 0 else 0

    return accuracy

def objective(trial):
    # Define the hyperparameters to tune
    conf_threshold = trial.suggest_float('conf_threshold', 0.3, 0.99)
    bbox_ratio_threshold = trial.suggest_float('bbox_ratio_threshold', 0.1, 0.89)
    
    # Directories containing good and bad photos
    good_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\optuna\Good"
    bad_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\optuna\Bad"

    accuracy = process_images(conf_threshold, bbox_ratio_threshold, good_dir, bad_dir)
    
    # Define a metric to maximize (e.g., the accuracy of classification)
    return accuracy

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)

print('Best trial:')
trial = study.best_trial
print(f'  Value: {trial.value}')
print(f'  Params: {trial.params}')
