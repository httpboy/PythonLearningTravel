# 爬取 豆瓣音乐音乐人分类 https://music.douban.com
from lxml import etree
import requests

url = 'https://music.douban.com/'  # 需要爬的网址
page = requests.Session().get(url)
htmlString = etree.HTML(page.text)
# print("page.text \n" + htmlString)
musicType = htmlString.xpath("//tr//a/text()")
musicUrl = htmlString.xpath("//tr//a/@href")
print("..........热门音乐人才分类..........")
print(musicType)
print("..........热门音乐URL..........")
print(musicUrl)
print("..........热门音乐URL进行自定义拼接..........")
for urlIndex in range(len(musicUrl)):
    if urlIndex >= 1:
        print(musicUrl[0].replace("ypy", "music") + musicUrl[urlIndex])
