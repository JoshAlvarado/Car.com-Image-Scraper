import requests

def test_proxy(proxy):
    try:
        response = requests.get(
            'https://www.cars.com/shopping/results/?body_style_slugs[]=sedan&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=all&mileage_max=&models[]=mercedes_benz-c_class&monthly_payment=&only_with_photos=true&page_size=100&sort=list_price_desc&stock_type=all&year_max=2020&year_min=2015&zip=91331',
            proxies={"http": proxy, "https": proxy},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def main():
    working_proxies = []

    with open('http_proxies.txt', 'r') as file:
        for line in file:
            proxy = line.strip()
            print(f"Testing proxy: {proxy}")
            if test_proxy(proxy):
                print("Proxy works!")
                working_proxies.append(proxy)
            else:
                print("Proxy failed.")

    with open('httpworkingproxie.txt', 'w') as file:
        for proxy in working_proxies:
            file.write(proxy + '\n')

    print("Finished testing proxies. Working proxies are saved in httpworkingproxie.txt")

if __name__ == "__main__":
    main()
