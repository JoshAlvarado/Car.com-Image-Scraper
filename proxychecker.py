import requests

def load_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

def test_proxy(proxy):
    test_url = 'https://www.cars.com/shopping/results/?stock_type=used&makes[]=mercedes_benz&models[]=mercedes_benz-c_class&list_price_max=&year_min=2015&year_max=2020&mileage_max=&zip=91331&sort=best_match_desc&per_page=20'
    try:
        response = requests.get(test_url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} is working.")
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def save_working_proxies(proxies, output_file):
    for proxy in proxies:
        if test_proxy(proxy):
            with open(output_file, 'a') as file:  # Open file in append mode
                file.write(proxy + '\n')

if __name__ == "__main__":
    proxy_file = 'C:/Users/joshu/OneDrive/Desktop/Car.com-Image-Scraper/http_proxies.txt'
    output_file = 'C:/Users/joshu/OneDrive/Desktop/Car.com-Image-Scraper/httpworkingproxies.txt'
    # Ensure the output file is empty before starting
    open(output_file, 'w').close()
    proxies = load_proxies_from_file(proxy_file)
    save_working_proxies(proxies, output_file)
