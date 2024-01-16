import requests
from bs4 import BeautifulSoup
import os
import hashlib
import time
from urllib.parse import urljoin
from requests.exceptions import RequestException
from socket import timeout as SocketTimeout
from urllib3.exceptions import ProtocolError

# Function to generate a hash for image content.
def get_image_hash(image_content):
    return hashlib.md5(image_content).hexdigest()

# Function to download an image with retries and proxy support.
def download_image_with_retries(img_url, file_path, proxies, max_retries=3, delay=1):
    retries = 0
    while retries < max_retries:
        try:
            proxy = proxies[retries % len(proxies)]
            response = requests.get(img_url, timeout=10, proxies={"http": proxy, "https": proxy})
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return True
        except (RequestException, ProtocolError, SocketTimeout) as e:
            print(f"Error downloading image {img_url} using proxy {proxy}: {e}")
            retries += 1
            time.sleep(delay)
    print(f"Failed to download image after {max_retries} retries: {img_url}")
    return False

# Function to scrape images and save them without duplicates with proxy support.
def scrape_images(base_url, model_code, target_directory, proxies, max_images=5000):
    downloaded_images = 0
    duplicate_images = 0
    page = 1
    downloaded_hashes = set()

    # Ensure the target directory exists and create if it does not.
    target_directory = os.path.join(target_directory, model_code)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    while downloaded_images < max_images:
        current_url = f"{base_url}&page={page}"
        page_response = requests.get(current_url)
        page_response.raise_for_status()

        page_soup = BeautifulSoup(page_response.text, 'html.parser')
        listing_links = [urljoin(current_url, a['href']) for a in page_soup.select('a.vehicle-card-link')]

        for listing_url in listing_links:
            if downloaded_images >= max_images:
                break

            listing_id = listing_url.split('/')[-2]
            print(f"Accessing listing: {listing_url}")

            listing_response = requests.get(listing_url)
            listing_response.raise_for_status()
            listing_soup = BeautifulSoup(listing_response.text, 'html.parser')
            image_tags = listing_soup.find_all('img', {'class': 'swipe-main-image'})
            image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]

            for img_url in image_urls:
                if downloaded_images >= max_images:
                    break

                image_response = requests.get(img_url)
                image_response.raise_for_status()
                image_content = image_response.content
                image_hash = get_image_hash(image_content)

                if image_hash in downloaded_hashes:
                    duplicate_images += 1
                    continue

                image_name = f"{listing_id}_Image_{downloaded_images}.jpg"
                image_path = os.path.join(target_directory, image_name)

                if download_image_with_retries(img_url, image_path, proxies):
                    downloaded_images += 1
                    downloaded_hashes.add(image_hash)

        page += 1

    print(f'Total images downloaded: {downloaded_images}')
    print(f'Total duplicate images skipped: {duplicate_images}')

# Example usage with proxy list
base_url = 'https://www.cars.com/shopping/results/?stock_type=used&makes[]=mercedes_benz&models[]=mercedes_benz-c_class&list_price_max=&year_min=2015&year_max=2020&mileage_max=&zip=91331&sort=best_match_desc&per_page=20'
model_code = 'W205'
target_directory = 'C:\\Users\\joshu\\OneDrive\\Desktop\\Car.com-Image-Scraper'
proxies = ['http://proxy1.example.com:port', 'http://proxy2.example.com:port']  # Add your proxy server addresses here
scrape_images(base_url, model_code, target_directory, proxies)
