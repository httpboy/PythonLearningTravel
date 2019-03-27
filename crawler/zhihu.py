import json

import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}
session = requests.Session()


def juejin_login(phonenumber, password):  # 登陆掘金

    login_data = {
        'phoneNumber': phonenumber,
        'password': password,
    }
    url = 'https://juejin.im/auth/type/phoneNumber'  # 登陆接口

    login_response = session.post(url, headers=headers, data=login_data)
    print(login_response.status_code)  # 打印状态码
    print("login_response:" + login_response.text)  # 打印内容
    login_json = json.loads(login_response.text)  # 将json格式的字符串转为python数据类型的对象
    print(login_json["token"])  # 打印token

    return login_json


def juejin_index(login_json):  # 爬取掘金首页内容

    index_data = {
        'src': 'web',
        'uid': login_json['user']['uid'],
        'device_id': login_json['clientId'],
        'token': login_json['token'],
        'limit': '20',
        'category': 'all',
        'recomment': '1',
    }
    index_response = session.get('https://timeline-merger-ms.juejin.im/v1/get_entry_by_rank?',
                                 headers=headers,
                                 params=index_data)
    print(index_response.status_code)
    print("index_response:" + index_response.text)


if __name__ == '__main__':
    json_dict = juejin_login('18159020779', 'cb8585204')
    juejin_index(json_dict)
