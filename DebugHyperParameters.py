import torch
from PIL import Image, UnidentifiedImageError
import os
import shutil
import optuna

def process_images(conf_threshold, bbox_ratio_min, bbox_ratio_max, good_dir, bad_dir):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True, trust_repo=True)
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
                continue

            results = model(img, size=640)
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

                if largest_conf >= conf_threshold and bbox_ratio_min <= bbox_ratio <= bbox_ratio_max:
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
    conf_threshold = trial.suggest_uniform('conf_threshold', 0.3, 0.99)
    bbox_ratio_min = trial.suggest_uniform('bbox_ratio_min', 0.1, 0.4)
    bbox_ratio_max = trial.suggest_uniform('bbox_ratio_max', 0.5, 0.9)

    good_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\optuna\Good"
    bad_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\optuna\Bad"

    accuracy = process_images(conf_threshold, bbox_ratio_min, bbox_ratio_max, good_dir, bad_dir)
    return accuracy

def main():
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=200)

    print('Best trial:')
    trial = study.best_trial
    print(f'  Value: {trial.value}')
    print(f'  Params: {trial.params}')

    conf_threshold = trial.params['conf_threshold']
    bbox_ratio_min = trial.params['bbox_ratio_min']
    bbox_ratio_max = trial.params['bbox_ratio_max']

    source_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205"
    cleaned_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\debugginghyperP\cleaned"
    discarded_dir = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\debugginghyperP\discarded"

    if not os.path.exists(cleaned_dir):
        os.makedirs(cleaned_dir)
    if not os.path.exists(discarded_dir):
        os.makedirs(discarded_dir)

    process_images(conf_threshold, bbox_ratio_min, bbox_ratio_max, source_dir, cleaned_dir, discarded_dir)

if __name__ == "__main__":
    main()
