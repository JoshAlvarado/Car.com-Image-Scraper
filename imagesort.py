import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk

# Define paths
source_folder = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205"
keep_folder = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205keep"
coup_folder = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205coup"
delete_folder = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\W205delete"

# Ensure target folders exist
os.makedirs(keep_folder, exist_ok=True)
os.makedirs(coup_folder, exist_ok=True)
os.makedirs(delete_folder, exist_ok=True)

# Get list of images
image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
current_index = 0
coup_base_names = set()

# Function to move image
def move_image(target_folder, action, base_name=None):
    global current_index
    if current_index < len(image_files):
        image_path = os.path.join(source_folder, image_files[current_index])
        shutil.move(image_path, target_folder)
        print(f"Image {image_files[current_index]} has been {action}.")
        
        if action == "moved to coup":
            base_name = base_name or get_base_name(image_files[current_index])
            coup_base_names.add(base_name)

        current_index += 1
        if current_index < len(image_files):
            show_image()
        else:
            print("All images have been processed.")
            app.quit()

# Function to get base name of an image file
def get_base_name(filename):
    return '_'.join(filename.split('_')[:-1])

# Function to show image
def show_image():
    global current_index
    image_path = os.path.join(source_folder, image_files[current_index])
    base_name = get_base_name(image_files[current_index])
    
    if base_name in coup_base_names:
        move_image(coup_folder, "automatically moved to coup", base_name)
    else:
        print(f"Now showing: {image_files[current_index]}")
        img = Image.open(image_path)
        img.thumbnail((800, 600))
        img = ImageTk.PhotoImage(img)
        panel.config(image=img)
        panel.image = img

# GUI setup
app = tk.Tk()
app.title("Image Sorter")

panel = tk.Label(app)
panel.pack(side="top", fill="both", expand="yes")

frame = tk.Frame(app)
frame.pack(side="bottom", fill="x")

btn_keep = tk.Button(frame, text="Keep", command=lambda: move_image(keep_folder, "kept"))
btn_keep.pack(side="left", fill="x", expand="yes")

btn_coup = tk.Button(frame, text="Move to Coup", command=lambda: move_image(coup_folder, "moved to coup"))
btn_coup.pack(side="left", fill="x", expand="yes")

btn_delete = tk.Button(frame, text="Move to Delete", command=lambda: move_image(delete_folder, "deleted"))
btn_delete.pack(side="left", fill="x", expand="yes")

show_image()
app.mainloop()
