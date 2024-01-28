import requests
import socks
import socket

# URL to test with
test_url = 'https://www.cars.com/shopping/results/?body_style_slugs[]=sedan&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=all&mileage_max=&models[]=mercedes_benz-c_class&monthly_payment=&only_with_photos=true&page_size=100&sort=list_price_desc&stock_type=all&year_max=2020&year_min=2015&zip=91331'  # Replace with the URL you want to test

def test_socks5_proxies_from_file(file_path, test_url):
    working_proxies = []

    try:
        with open(file_path, 'r') as proxy_file:
            proxies = [line.strip() for line in proxy_file]

        for proxy in proxies:
            try:
                proxy_address, proxy_port = proxy.split(':')
                proxy_port = int(proxy_port)

                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_address, proxy_port)
                socket.socket = socks.socksocket  # Use SOCKS proxy for all socket connections

                response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=2, verify=False)
  # Set timeout to 10 seconds for SOCKS proxy
                if response.status_code == 200:
                    print(f"SOCKS5 Proxy {proxy} is working correctly.")
                    working_proxies.append(proxy)
                else:
                    print(f"SOCKS5 Proxy {proxy} returned a non-200 status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"SOCKS5 Proxy {proxy} encountered an error: {e}")
            except ValueError:
                print(f"Invalid proxy format: {proxy}")

        # Write working SOCKS5 proxies to a new file
        with open('working_socks5_proxies.txt', 'w') as working_proxy_file:
            for working_proxy in working_proxies:
                working_proxy_file.write(working_proxy + '\n')

        print(f"Working SOCKS5 proxies saved to 'working_socks5_proxies.txt' file.")
    except FileNotFoundError:
        print(f"Proxy file not found: {file_path}")

if __name__ == "__main__":
    proxy_file_path = r'C:\Users\joshu\OneDrive\Desktop\Car.com-Image-Scraper\socks5_proxies.txt'
    test_socks5_proxies_from_file(proxy_file_path, test_url)
