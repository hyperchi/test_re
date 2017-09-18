# -*- coding: utf-8 -*-
import requests
import json
import base64
def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    postData = {
        'entry': 'sso',
        'gateway': '1',
        'from': 'null',
        'savestate': '30',
        'userticket': '0',
        'pagerefer': '',
        'vsnf': '1',
        'su': username,
        'service': 'sso',
        'sp': password,
        'sr': '1440*900',
        'encoding': 'UTF-8',
        'cdult': '3',
        'domain': 'sina.com.cn',
        'prelt': '0',
        'returntype': 'TEXT',
    }
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    session = requests.Session()
    res = session.post(loginURL, data = postData)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    print info
    if info["retcode"] == "0":
        print("Login success!")
        # add cookie to header!!!! this line is user important
        weibo_com_session = requests.Session()
        ret = weibo_com_session.get(info['crossDomainUrlList'][0])
        print("Return content:")
        print(ret.content)
        print("Checking cookie...")
        cookies = ret.cookies.get_dict('.weibo.com', '/')
        print cookies
        #cookies = [key + "=" + value for key, value in cookies.items()]
        #cookies = "; ".join(cookies)
        print("Cookie is:")
        print(cookies)
    else:
        print("Login failed，reason： %s" % info["reason"].encode("utf8"))
    return cookies

if __name__ == '__main__':
    with open("user.json", "rb") as f:
        data = json.loads(f.read())
    username = data["username"]
    password = data["password"]
    session = login(username, password)