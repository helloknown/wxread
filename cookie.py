import pprint

import requests
import json

def get_wr_skey(headers, cookies):
    url = "https://weread.qq.com/web/login/renewal"
    data = {
        "rq": "%2Fweb%2Fbook%2Fread"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    # print(response.text)
    cookie_str = response.headers['Set-Cookie']
    # print(cookie_str)
    wr_key = ""
    for cookie in cookie_str.split(';'):
        if cookie.__contains__("wr_skey"):
            wr_skey = cookie[-8:]
            print("数据初始化成功！")
            return wr_skey