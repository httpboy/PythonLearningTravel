# 爬取“房天下”租房信息 https://tj.zu.fang.com
import re

from lxml import etree
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
data = requests.get("https://tj.zu.fang.com/house1/", headers=headers)
print("..........房天下-地铁..........")
# print(data.text)
data.encoding = "gbk"
htmlString = etree.HTML(data.text)
# 获取房源图片
houseImgUrl = htmlString.xpath('//img[@class="b-lazy b-loaded"]/@src')
# 获取房源title
houseTitle = htmlString.xpath('//dl[@class="list hiddenMap rel"]//p/a/text()')
# 获取房源内容
hourseStr = ""
hourseList = []
houseContent = htmlString.xpath('//p[@class="font15 mt12 bold"]/text()')
for houseContentIndex in range(len(houseContent)):
    # 去除字符中间空格
    houseContent[houseContentIndex] = houseContent[houseContentIndex].replace(' ', '')
    if houseContent[houseContentIndex].find('\r\n') >= 0:
        houseContent[houseContentIndex] = houseContent[houseContentIndex].replace('\r\n', '')
    if houseContentIndex % 4 == 0:
        hourseStr += houseContent[houseContentIndex] + ""
        if houseContentIndex == 0:
            continue
        hourseList.append(hourseStr)


    else:
        hourseStr += houseContent[houseContentIndex] + "-"

# 获取房源价格
housePrice = htmlString.xpath('//div[@class="moreInfo"]//span/text()')
print("获取房源图片")
print(houseImgUrl)
print("获取房源title")
print(houseTitle)
print("获取房源内容")
print(hourseList)
print("获取房源价格")
print(housePrice)
