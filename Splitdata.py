import os
import shutil
import time

# Define the path to your main and test data directories
main_directory = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\Data"
testdata_directory = r"C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\Testdatas"

# List all the folders inside the main directory
folders = [f.name for f in os.scandir(main_directory) if f.is_dir()]

# Function to move files and update their "modified" timestamp
def move_files(src_folder, dest_folder, num_files_to_move):
    # Get all files in the source folder
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]

    # Move the required number of files from source to destination
    for file in files[:num_files_to_move]:
        src_file = os.path.join(src_folder, file)
        dest_file = os.path.join(dest_folder, file)
        shutil.move(src_file, dest_file)

        # Update the "modified" timestamp to the current time
        current_time = time.time()
        os.utime(dest_file, (current_time, current_time))

    print(f"Moved {len(files[:num_files_to_move])} files from {src_folder} to {dest_folder}")

# Iterate over each folder in the main directory
for folder in folders:
    src_folder = os.path.join(main_directory, folder)
    dest_folder = os.path.join(testdata_directory, folder)

    # Ensure the destination folder exists in the testdata directory
    os.makedirs(dest_folder, exist_ok=True)

    # Count the number of images in the destination folder
    existing_images = len([f for f in os.listdir(dest_folder) if os.path.isfile(os.path.join(dest_folder, f))])

    # Calculate how many more images are needed to reach 1,000
    images_needed = 1000 - existing_images

    # If more images are needed, move them
    if images_needed > 0:
        move_files(src_folder, dest_folder, images_needed)
    else:
        print(f"{dest_folder} already has 1,000 or more images, no files moved.")
