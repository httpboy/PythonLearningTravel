import json
import os

import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}
session = requests.Session()

global rankIndex
rankIndex = ""


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


def juejin_index(login_json, pams_rankIndex):  # 爬取掘金首页内容
    global rankIndex
    index_data = {
        'src': 'web',
        'uid': login_json['user']['uid'],
        'device_id': login_json['clientId'],
        'token': login_json['token'],
        'limit': '20',
        'category': 'all',
        'before': pams_rankIndex,
        'recomment': '1',
    }
    index_response = session.get('https://timeline-merger-ms.juejin.im/v1/get_entry_by_rank?',
                                 headers=headers,
                                 params=index_data)
    print(index_response.status_code)
    print("index_response:" + index_response.text)
    json_index_response = json.loads(index_response.text)
    entrylist = json_index_response['d']['entrylist']
    print(entrylist)
    sql_data_list = []  # 最后储存到数据的变量

    for i, item in enumerate(entrylist):
        if i + 1 == 20:
            rankIndex = item['rankIndex']
        sql_dict = {}
        tag_title = item['tags'][0]['title']
        print("文章类别：" + tag_title)
        username = item['user']['username']
        print("用户名：" + username)
        jobTitle = item['user']['jobTitle']
        print("大厂title：" + jobTitle)
        contentTitle = item['title']
        print("文章标题：" + contentTitle)
        summaryInfo = item['summaryInfo']
        print("文章简介：" + summaryInfo)
        collectionCount = item['collectionCount']
        print("文章收藏数：" + str(collectionCount))
        print("-------------------------------------------------")
        sql_dict["username"] = username
        sql_dict["tag_title"] = tag_title
        sql_dict["jobTitle"] = jobTitle
        sql_dict["contentTitle"] = contentTitle
        sql_dict["summaryInfo"] = summaryInfo
        sql_dict["collectionCount"] = collectionCount
        sql_data_list.append(sql_dict)
        print("---------------------打印sql_data_list列表----------------------------")
        # print(sql_data_list)
        return sql_data_list


def saveToLocalJson(sql_data):  # 保存到json文件中
    json_data = json.dumps(sql_data)  # 将 Python 对象编码成 JSON 字符串
    txt_file_path = os.path.split(os.path.realpath(__file__))[0] + "/sql.json"  # 这是保存txt文件的位置
    print("数据存储路径：" + txt_file_path)
    file = open(txt_file_path, 'w')
    file.write(json_data)
    file.close()


if __name__ == '__main__':
    json_dict = juejin_login('XXX', 'XXX')  # 登陆成功
    page = 0  # 初始化页数，TOP一共有250部   每页25部
    while page <= 20:
        page += 20
        sql_data_list = juejin_index(json_dict, rankIndex)  # 获取sql_data_list列表
        saveToLocalJson(sql_data_list)
