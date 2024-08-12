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
        image_name = image_files[current_index]
        base_name = base_name or get_base_name(image_name)
        
        if target_folder == coup_folder:
            # Check and move all related files from keep_folder to coup_folder
            for file in os.listdir(keep_folder):
                if get_base_name(file) == base_name:
                    shutil.move(os.path.join(keep_folder, file), coup_folder)
                    print(f"Image {file} was kept before but has now been moved to coup.")
                    
            # Move the current image
            shutil.move(image_path, target_folder)
            print(f"Image {image_name} has been {action}.")
            coup_base_names.add(base_name)
        else:
            shutil.move(image_path, target_folder)
            print(f"Image {image_name} has been {action}.")

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
        print(f"Image {image_files[current_index]} has been automatically moved to coup.")
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

# Set dark mode colors
bg_color = "#2e2e2e"
fg_color = "#ffffff"
button_bg_color = "#3c3c3c"
button_fg_color = "#ffffff"

app.configure(bg=bg_color)

panel = tk.Label(app, bg=bg_color)
panel.pack(side="top", fill="both", expand="yes")

frame = tk.Frame(app, bg=bg_color)
frame.pack(side="bottom", fill="x")

btn_keep = tk.Button(frame, text="Keep", command=lambda: move_image(keep_folder, "kept"),
                     bg=button_bg_color, fg=button_fg_color)
btn_keep.pack(side="left", fill="x", expand="yes")

btn_coup = tk.Button(frame, text="Move to Coup", command=lambda: move_image(coup_folder, "moved to coup"),
                     bg=button_bg_color, fg=button_fg_color)
btn_coup.pack(side="left", fill="x", expand="yes")

btn_delete = tk.Button(frame, text="Move to Delete", command=lambda: move_image(delete_folder, "deleted"),
                       bg=button_bg_color, fg=button_fg_color)
btn_delete.pack(side="left", fill="x", expand="yes")

# Update text colors
app.option_add("*Label.foreground", fg_color)
app.option_add("*Button.foreground", fg_color)

show_image()
app.mainloop()
