import requests
from bs4 import BeautifulSoup
import os
import hashlib
import time
from urllib.parse import urljoin
from requests.exceptions import RequestException

def load_proxies_from_file(file_path='http_proxies.txt'):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

def get_image_hash(image_content):
    return hashlib.md5(image_content).hexdigest()

def download_image_with_retries(img_url, file_path, proxies, max_retries=3, delay=1):
    bad_proxies = set()
    for proxy in proxies:
        if proxy in bad_proxies:
            continue
        print(f"Trying proxy: {proxy}")
        try:
            response = requests.get(img_url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print("Image downloaded successfully with proxy:", proxy)
            return True
        except RequestException as e:
            print(f"Error with proxy {proxy}: {e}")
            bad_proxies.add(proxy)
            time.sleep(delay)
    print(f"Failed to download image after trying all proxies: {img_url}")
    return False

def get_image_urls(listing_url, proxies):
    # Here's an update to use a rotating proxy for fetching listing pages
    for proxy in proxies:
        try:
            response = requests.get(listing_url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return [img['src'] for img in soup.find_all('img') if 'src' in img.attrs and 'swipe-main-image' in img.attrs.get('class', '')]
        except RequestException:
            continue  # Try the next proxy if one fails
    return []  # Return an empty list if all proxies fail or no images are found

def scrape_images(base_url, model_code, target_directory, proxies, max_images=5000):
    print('Starting scraper')
    downloaded_images = 0
    page = 1
    downloaded_hashes = set()

    target_directory = os.path.join(target_directory, model_code)
    os.makedirs(target_directory, exist_ok=True)

    while downloaded_images < max_images:
        current_url = f"{base_url}&page={page}"
        print(f"Fetching URL: {current_url}")
        search_page_response = requests.get(current_url, timeout=5)  # Consider using proxies here as well
        if search_page_response.status_code == 200:
            search_page_soup = BeautifulSoup(search_page_response.content, 'html.parser')
            listing_links = [urljoin(current_url, a['href']) for a in search_page_soup.select('a.vehicle-card-link[href]')]
            for listing_url in listing_links:
                print(f"Accessing listing: {listing_url}")
                image_urls = get_image_urls(listing_url, proxies)
                for img_url in image_urls:
                    image_hash = get_image_hash(requests.get(img_url).content)
                    if image_hash in downloaded_hashes:
                        continue
                    image_name = f"{image_hash}.jpg"
                    image_path = os.path.join(target_directory, image_name)
                    if download_image_with_retries(img_url, image_path, proxies):
                        downloaded_images += 1
                        downloaded_hashes.add(image_hash)
                        if downloaded_images >= max_images:
                            break
        else:
            print(f"Failed to fetch search page: {current_url}")
        page += 1
        if downloaded_images >= max_images:
            break

    print(f'Total images downloaded: {downloaded_images}')

if __name__ == "__main__":
    print("Starting the scraper")
    base_url = 'https://www.cars.com/shopping/results/?stock_type=used&makes[]=mercedes_benz&models[]=mercedes_benz-c_class&list_price_max=&year_min=2015&year_max=2020&mileage_max=&zip=91331&sort=best_match_desc&per_page=20'
    model_code = 'W205'
    target_directory = 'C:\\Users\\joshu\\OneDrive\\Desktop\\Car.com-Image-Scraper'
    proxies = load_proxies_from_file('http_proxies.txt')
    scrape_images(base_url, model_code, target_directory, proxies)
