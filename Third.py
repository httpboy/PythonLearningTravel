from time import sleep

from selenium import webdriver

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get("http://www.baidu.com")
    print(browser.page_source)
    # browser.close()
    webElement = browser.find_element_by_id("kw")
    webElement.send_keys("请您打开微信！关注微信公众号：开发者技术圈")
    sleep(2)
    browser.find_element_by_id("su").click()
