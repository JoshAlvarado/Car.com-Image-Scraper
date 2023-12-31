import requests
from bs4 import BeautifulSoup
import os
import hashlib
import urllib.request
from urllib.parse import urljoin

# Function to generate a hash for image content.
def get_image_hash(image_content):
    return hashlib.md5(image_content).hexdigest()

# Function to scrape images and save them without duplicates.
def scrape_images(base_url, model_code, target_directory, max_images=2000):
    downloaded_images = 0
    page = 1
    downloaded_hashes = set()

    # Ensure the target directory exists and create if it does not.
    target_directory = os.path.join(target_directory, model_code)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    print(f"Images will be saved in: {target_directory}")

    # Loop through pages until the maximum number of images is reached.
    while downloaded_images < max_images:
        current_url = f"{base_url}&page={page}"
        page_response = requests.get(current_url)
        page_response.raise_for_status()

        page_soup = BeautifulSoup(page_response.text, 'html.parser')

        # Find links to individual car listings on the current page.
        listing_links = [urljoin(current_url, a['href']) for a in page_soup.select('a.vehicle-card-link')]

        for listing_url in listing_links:
            if downloaded_images >= max_images:
                break

            # Extract the unique identifier from the listing URL.
            listing_id = listing_url.split('/')[-2]
            print(f"Accessing listing: {listing_url}")  # Print the listing URL

            listing_response = requests.get(listing_url)
            listing_response.raise_for_status()

            listing_soup = BeautifulSoup(listing_response.text, 'html.parser')

            # Find all image URLs on the listing page.
            image_tags = listing_soup.find_all('img', {'class': 'swipe-main-image'})
            image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]

            # Image counter for each individual listing.
            image_counter = 0

            for img_url in image_urls:
                if downloaded_images >= max_images:
                    break

                # Fetch the image content without downloading.
                image_response = requests.get(img_url)
                image_response.raise_for_status()
                image_content = image_response.content
                image_hash = get_image_hash(image_content)

                # Check if we have already downloaded this image.
                if image_hash in downloaded_hashes:
                    print(f"Duplicate image found. Skipping: {img_url}")
                    continue

                # Save the image content and update the hash set.
                try:
                    image_name = f"{listing_id}_Image_{image_counter}.jpg"
                    image_path = os.path.join(target_directory, image_name)
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_content)
                    print(f"Image saved at {image_path}")
                    downloaded_images += 1
                    image_counter += 1
                    downloaded_hashes.add(image_hash)
                except Exception as e:
                    print(f"Failed to download image {img_url}: {e}")

        print(f'Finished page {page}. Total images downloaded so far: {downloaded_images}')
        page += 1

    print(f'Total images downloaded: {downloaded_images}')

# Example usage of the function.
base_url = 'https://www.cars.com/shopping/results/?stock_type=used&makes[]=mercedes_benz&models[]=mercedes_benz-c_class&list_price_max=&year_min=2015&year_max=2020&mileage_max=&zip=91331&sort=best_match_desc&per_page=20'
model_code = 'W205'
target_directory = 'C:\\Users\\joshu\\OneDrive\\Desktop\\Car.com-Image-Scraper'
scrape_images(base_url, model_code, target_directory)
