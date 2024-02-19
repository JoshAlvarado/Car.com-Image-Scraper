import torch
from PIL import Image

# Function to load an image from a file
def load_image_from_file(file_path):
    img = Image.open(file_path)
    return img, img.size

def main():
    # Load the model from the official YOLOv5 repository
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()

    # Load image from local file
    img_path = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\Debugging\75e673ee-d25e-4968-ab31-c4e95344d4c6_2.jpg"
    img, (width, height) = load_image_from_file(img_path)

    # Perform detection
    results = model(img)

    # Display results
    results.show()  # or .save(), .print(), etc.

    # Initialize variable to track the largest box
    largest_box_area = 0

    # Filter for cars and print results
    for *box, conf, cls in results.xyxy[0]:
        if results.names[int(cls)] == 'car':
            print(f"Car detected: {box} with confidence {conf}")

            # Calculate the area of the box
            x1, y1, x2, y2 = box
            box_area = (x2 - x1) * (y2 - y1)
            largest_box_area = max(largest_box_area, box_area)

    # Calculate and print the percentage of the image occupied by the largest box
    img_area = width * height
    if largest_box_area > 0:
        occupied_percentage = (largest_box_area / img_area) * 100
        print(f"The largest car box occupies {occupied_percentage:.2f}% of the image.")

if __name__ == "__main__":
    main()
