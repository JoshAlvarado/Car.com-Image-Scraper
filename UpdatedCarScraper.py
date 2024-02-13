import requests
from bs4 import BeautifulSoup
import os
import hashlib
import time
from urllib.parse import urljoin
from requests.exceptions import ProxyError, ConnectTimeout, HTTPError

# Load proxies from file
def load_proxies_from_file(file_path='http_proxies.txt'):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

# Get image hash
def get_image_hash(image_content):
    return hashlib.md5(image_content).hexdigest()

# Download image with retries, moving to the next proxy on failure
def download_image(img_url, file_path, proxies):
    for proxy in proxies:
        try:
            print(f"Trying proxy: {proxy}")
            response = requests.get(img_url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
            response.raise_for_status()  # Check for HTTP errors
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print("Image downloaded successfully with proxy:", proxy)
            return True
        except (ProxyError, ConnectTimeout, HTTPError) as e:
            print(f"Error with proxy {proxy}: {e}. Trying next proxy.")
    print(f"Failed to download image after trying all proxies: {img_url}")
    return False

# Main scraping function
def scrape_images(base_url, model_code, target_directory, proxies, max_images=5000):
    downloaded_images = 0
    downloaded_hashes = set()
    target_directory = os.path.join(target_directory, model_code)
    os.makedirs(target_directory, exist_ok=True)

    # Assuming this fetches a list of image URLs
    image_urls = []  # Placeholder for where you'd fetch image URLs

    for img_url in image_urls:
        image_hash = get_image_hash(requests.get(img_url).content)
        if image_hash in downloaded_hashes:
            continue
        image_name = f"{image_hash}.jpg"
        image_path = os.path.join(target_directory, image_name)
        if download_image(img_url, image_path, proxies):
            downloaded_images += 1
            downloaded_hashes.add(image_hash)
            if downloaded_images >= max_images:
                break

    print(f'Total images downloaded: {downloaded_images}')

if __name__ == "__main__":
    base_url = 'https://www.cars.com/shopping/results/?stock_type=used&makes[]=mercedes_benz&models[]=mercedes_benz-c_class&list_price_max=&year_min=2015&year_max=2020&mileage_max=&zip=91331&sort=best_match_desc&per_page=20'
    model_code = 'W205'
    target_directory = 'C:\\Users\\joshu\\OneDrive\\Desktop\\Car.com-Image-Scraper'
    proxies = load_proxies_from_file('http_proxies.txt')
    scrape_images(base_url, model_code, target_directory, proxies)
