import torch
from PIL import Image, ImageDraw, ImageFont
import random

# Function to load an image from a file
def load_image_from_file(file_path):
    img = Image.open(file_path)
    return img, img.size

# Predefined list of distinct colors and their RGB values
color_names = [
    ("red", (255, 0, 0)),
    ("green", (0, 255, 0)),
    ("blue", (0, 0, 255)),
    ("yellow", (255, 255, 0)),
    ("magenta", (255, 0, 255)),
    ("cyan", (0, 255, 255)),
    ("orange", (255, 165, 0)),
    ("purple", (128, 0, 128)),
    ("pink", (255, 192, 203)),
    ("brown", (165, 42, 42))
]

def main():
    # Load the model from the official YOLOv5 repository
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device).eval()

    # Load image from local file
    img_path = r"c:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\Debuggingbelow20box\cleaned\c6aa7af4-1da7-42e5-8fec-eacfca8cb8f6_5.jpg"
    img, (width, height) = load_image_from_file(img_path)

    # Perform detection
    results = model(img)

    # Initialize variable to track the largest box
    largest_box_area = 0
    img_draw = ImageDraw.Draw(img)

    # Define a font
    font = ImageFont.load_default()

    # Filter for cars and print results
    for i, (*box, conf, cls) in enumerate(results.xyxy[0]):
        if results.names[int(cls)] == 'car':
            x1, y1, x2, y2 = [int(coord.item()) for coord in box]
            box_area = (x2 - x1) * (y2 - y1)
            largest_box_area = max(largest_box_area, box_area)

            # Assign a distinct color to the box
            color_name, box_color = color_names[i % len(color_names)]
            img_draw.rectangle([x1, y1, x2, y2], outline=box_color, width=2)

            # Calculate the percentage of the image occupied by the box
            img_area = width * height
            occupied_percentage = (box_area / img_area) * 100

            # Text to display
            text = f"{conf:.2f}, {occupied_percentage:.2f}%"

            # Get the size of the text
            text_bbox = img_draw.textbbox((x1, y1), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_position = (x1, y1 - text_height)

            # Draw the text background
            img_draw.rectangle([text_position, (x1 + text_width, y1)], fill=box_color)
            img_draw.text(text_position, text, fill="black", font=font)

            print(f"Car {i+1}:")
            print(f"  Box coordinates: ({x1}, {y1}), ({x2}, {y2})")
            print(f"  Confidence: {conf:.2f}")
            print(f"  Box area: {box_area} pixels")
            print(f"  Box color: {color_name}")
            print(f"  Occupies {occupied_percentage:.2f}% of the image.")
            print("")

    # Display results
    img.show()  # or .save(), .print(), etc.

if __name__ == "__main__":
    main()
