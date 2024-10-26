import requests

#pushplus
# def push(content):
#     url = "https://www.pushplus.plus/send"
#     params = {
#         "token": "官网上去复制token",
#         "content": content
#     }
#     headers = {
#         'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
#     }

#     response = requests.get(url, headers=headers, params=params)
#     print(response.text)


#Server酱
def sc_send(sendkey, title, desp='', options=None):
    if sendkey is None:
        return
    if options is None:
        options = {}
    # 判断 sendkey 是否以 'sctp' 开头，并提取数字构造 URL
    if sendkey.startswith('sctp'):
        match = re.match(r'sctp(\d+)t', sendkey)
        if match:
            num = match.group(1)
            url = f'https://{num}.push.ft07.com/send/{sendkey}.send'
        else:
            raise ValueError('Invalid sendkey format for sctp')
    else:
        url = f'https://sctapi.ftqq.com/{sendkey}.send'
    params = {
        'title': title,
        'desp': desp,
        **options
    }
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.post(url, json=params, headers=headers)
    result = response.json()
    return result
