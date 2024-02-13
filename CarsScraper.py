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
    success_proxy = None
    attempts = 0

    while attempts < max_retries:
        proxy = success_proxy if success_proxy else proxies[0]  # Use last successful proxy or the first one if none
        if proxy in bad_proxies:
            proxies.remove(proxy)  # Remove bad proxy from the list
            if not proxies:  # If no proxies are left, break out of the loop
                break
            success_proxy = None  # Reset success_proxy since the current one is bad
            continue  # Skip to the next iteration to try with a new proxy

        print(f"Trying proxy: {proxy}")
        try:
            response = requests.get(img_url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print("Image downloaded successfully with proxy:", proxy)
            success_proxy = proxy  # Set this proxy as the last successful one
            return True
        except RequestException as e:
            print(f"Error with proxy {proxy}: {e}")
            bad_proxies.add(proxy)
            if success_proxy:  # If there was a successful proxy before, remove it since it's now failed
                proxies.remove(success_proxy)
            success_proxy = None  # Reset success_proxy since it failed
            attempts += 1
            time.sleep(delay)
    
        
    
    print(f"Failed to download image after {max_retries} attempts: {img_url}")
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
    page = 3
    downloaded_hashes = set()  # Set to store unique hashes of downloaded images

    target_directory = os.path.join(target_directory, model_code)
    os.makedirs(target_directory, exist_ok=True)

    while downloaded_images < max_images:
        current_url = f"{base_url}&page={page}"
        print(f"Fetching URL: {current_url}")
        search_page_response = requests.get(current_url, timeout=5)
        if search_page_response.status_code == 200:
            search_page_soup = BeautifulSoup(search_page_response.content, 'html.parser')
            listing_links = [urljoin(current_url, a['href']) for a in search_page_soup.select('a.vehicle-card-link[href]')]
            for listing_url in listing_links:
                listing_id = listing_url.split('/')[-2]
                # Check if any image for this listing already exists
                existing_images = [img for img in os.listdir(target_directory) if img.startswith(listing_id)]
                if existing_images:
                    print(f"Images for listing {listing_id} already exist, skipping entire listing.")
                    continue  # Skip to the next listing

                print(f"Accessing listing: {listing_url}")
                image_urls = get_image_urls(listing_url, proxies)
                for img_url in image_urls:
                    try:
                        img_response = requests.get(img_url, timeout=5)
                        img_response.raise_for_status()
                        image_hash = get_image_hash(img_response.content)
                        if image_hash in downloaded_hashes:
                            print(f"Duplicate image detected by hash, skipping: {img_url}")
                            continue  # Skip this image
                        image_name = f"{listing_id}_{len(existing_images) + 1}.jpg"
                        image_path = os.path.join(target_directory, image_name)
                        with open(image_path, 'wb') as f:
                            f.write(img_response.content)
                        downloaded_images += 1
                        downloaded_hashes.add(image_hash)
                        existing_images.append(image_name)  # Update the list to reflect the newly downloaded image
                        print(f"Downloaded {image_name}")
                        if downloaded_images >= max_images:
                            break
                    except RequestException as e:
                        print(f"Failed to download image: {e}")
        else:
            print(f"Failed to fetch search page: {current_url}")
        page += 1
        if downloaded_images >= max_images:
            break

    print(f'Total images downloaded: {downloaded_images}')

if __name__ == "__main__":
    print("Starting the scraper")
    base_url = 'https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=all&mileage_max=&models[]=mercedes_benz-c_class&monthly_payment=&only_with_photos=true&page_size=100&sort=best_match_desc&stock_type=used&year_max=2020&year_min=2015&zip=91331'
    model_code = 'W205'
    target_directory = 'C:\\Users\\joshu\\OneDrive\\Desktop\\Car.com-Image-Scraper'
    proxies = load_proxies_from_file('http_proxies.txt')
    scrape_images(base_url, model_code, target_directory, proxies)
