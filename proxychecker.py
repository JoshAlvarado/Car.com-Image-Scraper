import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_proxy(proxy):
    url = "https://www.cars.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    try:
        print(f"Testing proxy: {proxy}")
        response = requests.get(url, proxies=proxies, headers=headers, timeout=20, verify=False)
        print(f"Response status code: {response.status_code}")
        print(f"Response content length: {len(response.text)}")
        if response.status_code == 200:
            if "cars.com" in response.text.lower():
                print(f"Proxy {proxy} is working and returned the expected content.")
                return proxy
            else:
                print(f"Proxy {proxy} returned a 200 status, but the expected content was not found.")
        else:
            print(f"Proxy {proxy} returned a non-200 status code.")
    except requests.exceptions.RequestException as e:
        print(f"Error with proxy {proxy}: {str(e)}")
    return None

def main():
    with open('proxy.txt', 'r') as f:
        proxies = f.read().splitlines()

    print(f"Total proxies to check: {len(proxies)}")

    working_proxies = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(future_to_proxy):
            result = future.result()
            if result:
                working_proxies.append(result)
                print(f"Working proxy found: {result}")

    with open('workingproxy.txt', 'w') as f:
        for proxy in working_proxies:
            f.write(f"{proxy}\n")

    print(f"Total working proxies: {len(working_proxies)}")

if __name__ == "__main__":
    main()