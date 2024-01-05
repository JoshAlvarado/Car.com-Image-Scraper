import requests
from bs4 import BeautifulSoup
import os
import urllib.request
from urllib.parse import urljoin

def scrape_images(base_url, model_code, target_directory, max_images=2000):
    downloaded_images = 0
    page = 1

    # Ensure the target directory exists
    target_directory = os.path.join(target_directory, model_code)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    print(f"Images will be saved in: {target_directory}")

    while downloaded_images < max_images:
        current_url = f"{base_url}&page={page}"
        page_response = requests.get(current_url)
        page_response.raise_for_status()

        page_soup = BeautifulSoup(page_response.text, 'html.parser')

        # Find links to individual car listings on the current page
        listing_links = [urljoin(current_url, a['href']) for a in page_soup.select('a.vehicle-card-link')]

        for listing_url in listing_links:
            if downloaded_images >= max_images:
                break

            print(f"Accessing listing: {listing_url}")  # Print the listing URL
            listing_response = requests.get(listing_url)
            listing_response.raise_for_status()

            listing_soup = BeautifulSoup(listing_response.text, 'html.parser')

            # Find all image URLs on the listing page
            image_tags = listing_soup.find_all('img', {'class': 'swipe-main-image'})
            image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]

            for img_url in image_urls:
                if downloaded_images >= max_images:
                    break

                # Download the image
                try:
                    image_path = os.path.join(target_directory, f'image_{downloaded_images}.jpg')
                    urllib.request.urlretrieve(img_url, image_path)
                    print(f"Image {downloaded_images} saved at {image_path}")
                    downloaded_images += 1
                except Exception as e:
                    print(f"Failed to download image {img_url}: {e}")

        print(f'Finished page {page}. Total images downloaded so far: {downloaded_images}')
        page += 1

    print(f'Total images downloaded: {downloaded_images}')

# Example usage
base_url = 'https://www.cars.com/shopping/results/?stock_type=used&makes[]=mercedes_benz&models[]=mercedes_benz-c_class&list_price_max=&year_min=2015&year_max=2020&mileage_max=&zip=91331&sort=best_match_desc&per_page=20'
model_code = 'W205'
target_directory = 'C:\\Users\\joshu\\OneDrive\\Desktop\\Car.com-Image-Scraper'
scrape_images(base_url, model_code, target_directory)
