import requests
from bs4 import BeautifulSoup
import os
import time
import re
import urllib3
import itertools
import random
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_proxies():
    with open('workingproxy.txt', 'r') as f:
        return f.read().splitlines()

def try_request(url, headers, proxy=None):
    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None
    try:
        response = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=20)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error with proxy {proxy}: {str(e)}" if proxy else "Error without proxy.")
        return None

def get_listings(url, proxies, proxy_cycle):
    print(f"Fetching listings from page: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    attempts = 0
    while attempts < len(proxies) + 1:  # +1 for the final non-proxy attempt
        proxy = next(proxy_cycle)
        response = try_request(url, headers, proxy)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = soup.find_all('a', class_='vehicle-card-link js-gallery-click-link')
            if listings:
                print(f"Found {len(listings)} listings using proxy {proxy}.")
                return [f"https://www.cars.com{listing['href']}" for listing in listings]
            else:
                print(f"No listings found with proxy {proxy}.")
        attempts += 1
    return []

def download_images(url, save_directory, proxies, proxy_cycle, image_count):
    car_id = url.split('/')[-2]
    print(f"Processing listing with ID: {car_id}")
    
    # Check if images for this listing ID already exist
    if any(fname.startswith(car_id) for fname in os.listdir(save_directory)):
        print(f"Images for listing ID {car_id} already exist. Skipping.")
        return image_count

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    max_retries = 3
    for attempt in range(max_retries):
        proxy = next(proxy_cycle)
        response = try_request(url, headers, proxy)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            vdp_gallery = soup.find('vdp-gallery')
            if vdp_gallery and 'media-count' in vdp_gallery.attrs:
                media_count = int(vdp_gallery['media-count'])
                print(f"Media count for listing {car_id}: {media_count}")
                
                # Skip listing if media count is 3 or below
                if (media_count is None) or media_count <= 5:
                    print(f"Skipping listing {car_id} due to low media count ({media_count} images).")
                    return image_count
            else:
                print(f"Couldn't find media count for listing {car_id}. Skipping.")
                return image_count

            img_tags = soup.find_all('img')
            print(f"Found {len(img_tags)} image tags.")
            
            counter = 1
            for img in img_tags:
                if counter > media_count:
                    print(f"Reached media count limit for listing {car_id}. Moving to next listing.")
                    break

                img_url = img.get('src')
                if img_url and img_url.startswith('http'):
                    try:
                        img_data = requests.get(img_url, timeout=10).content
                        img_filename = os.path.join(save_directory, f'{car_id}_{counter}.jpg')
                        with open(img_filename, 'wb') as handler:
                            handler.write(img_data)
                        print(f"Downloaded {img_filename}")
                        counter += 1
                        image_count += 1

                        # Introduce a random delay between 0.5 and 1 second
                        time.sleep(random.uniform(0.1, .3))
                    except Exception as e:
                        print(f"Failed to download image {counter} from listing {car_id}: {e}")
                else:
                    print(f"Skipping image {counter} from listing {car_id}: Invalid URL or not an HTTP link")
            
            print(f"Downloaded {counter-1} images from listing {car_id}")
            return image_count

        # If the proxy fails, remove it from the list and switch to a new one
        print(f"Removing failed proxy {proxy} after {attempt+1} attempts.")
        proxies.remove(proxy)
        if not proxies:
            print("No more proxies available. Exiting.")
            return image_count
        proxy_cycle = itertools.cycle(proxies)  # Reset the cycle to avoid stale iterator
    
    # If all retries with all proxies fail, skip the listing
    print(f"Failed to fetch listing {car_id} after {max_retries} attempts. Skipping.")
    return image_count

def rotate_proxies(proxies, image_count):
    if image_count >= 120:
        print(f"Rotating proxy after downloading {image_count} images.")
        return itertools.cycle(proxies), 0
    return itertools.cycle(proxies), image_count

def update_url_with_page(url, page_number):
    """Update the given URL with the specified page number."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['page'] = [str(page_number)]  # Set the page parameter
    new_query_string = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query_string))
    return new_url

def main():
    # Variable for the car type, which will be used to create the subfolder
    car_type = 'L34'  # Change this value for different car types (e.g., 'w205', 'w204', etc.)
    
    base_url = "https://www.cars.com/shopping/results/?clean_title=true&dealer_id=&include_shippable=true&keyword=&list_price_max=&list_price_min=&makes[]=nissan&maximum_distance=all&mileage_max=&models[]=nissan-altima&monthly_payment=&only_with_photos=true&page=1&page_size=100&sort=list_price_desc&stock_type=all&year_max=&year_min=2019&zip=91331"

    # Define the save directory, including the car type subfolder
    base_directory = os.path.dirname(os.path.abspath(__file__))  # Base directory where the script is located
    save_directory = os.path.join(base_directory, car_type)  # Subfolder for the car type
    os.makedirs(save_directory, exist_ok=True)

    proxies = get_proxies()  # Load proxies from file
    proxy_cycle = itertools.cycle(proxies)
    
    # Start with a random proxy
    random_start = random.randint(0, len(proxies) - 1)
    proxy = proxies[random_start]

    image_count = 0

    page = 1
    while True:
        filter_url = update_url_with_page(base_url, page)
        listings = get_listings(filter_url, proxies, proxy_cycle)
        print(f"Found {len(listings)} listings on page {page}.")

        if not listings:
            print(f"No more listings found on page {page}. Stopping scraper.")
            break

        for listing in listings:
            image_count = download_images(listing, save_directory, proxies, proxy_cycle, image_count)

            # Rotate proxies if the download count exceeds 500
            proxy_cycle, image_count = rotate_proxies(proxies, image_count)

        page += 1  # Move to the next page

if __name__ == "__main__":
    main()
