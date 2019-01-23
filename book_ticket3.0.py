from time import sleep
import urllib.request
import ssl

from splinter import Browser

'''
作者：pk哥
公众号：Python知识圈
日期：2019/01/11
代码解析详见公众号「Python知识圈」文章。

建了一个火车票助力群，方便大家讨论抢票技术和互相加速助力抢票，想进群的话，欢迎关注公众号，加我微信，备注 12306，备注 12306，备注 12306，拉你进群
'''


# 实现自动购票的类
class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, username, passwd, order, passengers, dtime, starts, ends):
        self.username = username
        self.passwd = passwd
        self.order = order  # 车次，0代表所有车次
        self.passengers = passengers  # 乘客名
        self.starts = starts  # 起始地和终点
        self.ends = ends
        self.dtime = dtime  # 日期
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver_name = 'chrome'
        # self.executable_path = 'E:\py3\chromedriver.exe'

    # 登录功能实现
    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name', self.username)
        # sleep(1)
        self.driver.fill('userDTO.password', self.passwd)
        # sleep(1)
        print('请手动输入验证码并手动点击登录按钮...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

    def check_ticket(self, seat_type):
        print('开始购票...')  # 加载查询信息
        self.driver.cookies.add({"_jc_save_fromStation": self.starts})
        self.driver.cookies.add({"_jc_save_toStation": self.ends})
        self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
        self.driver.reload()
        count = 0
        if self.order != 0:
            while self.driver.url == self.ticket_url:
                self.driver.find_by_text('查询').click()
                count += 1
                print('第%d次点击查询...' % count)
                try:
                    self.driver.find_by_text('预订')[self.order - 1].click()
                    sleep(1.5)
                except Exception as e:
                    print(e)
                    print('预订失败...')
                    continue
        else:
            while self.driver.url == self.ticket_url:
                self.driver.find_by_text('查询').click()
                count += 1
                print('第%d次点击查询...' % count)
                try:
                    for i in self.driver.find_by_text('预订'):
                        i.click()
                        sleep(1.5)
                except Exception as e:
                    print(e)
                    print('预订失败...')
                    continue
        print('开始预订...')
        sleep(1)
        print('开始选择用户...')
        for p in self.passengers:
            self.driver.find_by_text(p).last.click()
            sleep(0.5)
            if p[-1] == ')':
                self.driver.find_by_id('dialog_xsertcj_ok').click()
        type = self.driver.find_by_id('seatType_1')
        type.find_by_tag('option')
        sleep(0.5)
        while True:
            if type.find_by_value(seat_type):  # 修改对应座次的 value 值，M 表示一等座，其他对应值详见公众号「Python知识圈」文章
                type.find_by_value(seat_type).click()  # 修改对应座次的 value 值，M 表示一等座，其他对应值详见公众号「Python知识圈」文章
                break
            self.driver.visit(self.ticket_url)
            self.check_ticket(seat_type)

    # 买票功能实现
    def start_buy(self):
        self.driver = Browser(driver_name=self.driver_name)
        # 窗口最大化
        self.driver.driver.maximize_window()
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            self.check_ticket(seat_type)
            print('成功选座！！！')
            sleep(0.5)
            print('提交订单...')
            self.driver.find_by_id('submitOrder_id').click()
            sleep(0.5)
            print('确认选座...')
            sleep(0.5)
            self.driver.find_by_id('qr_submit_id').click()
            print('预订成功...')
            sleep(5)
        except Exception as e:
            print(e)


def get_cookie(start, end):
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9058'
    context = ssl._create_unverified_context()
    result = urllib.request.urlopen(url, context=context).read().decode('utf8')
    result = result.replace('var station_names =\'', '').replace('\'', '').replace(';', '')
    station = result.split('@')
    from_ = ''
    to_ = ''
    for s in station:
        if not from_ and start in s:
            from_ = s.split('|')[2]
        elif not to_ and end in s:
            to_ = s.split('|')[2]
    if not from_ or not to_:
        print('车站输入错误！')
        return None, None
    from_ = start.encode('unicode_escape').decode().replace('\\', '%') + '%2c' + from_
    to_ = end.encode('unicode_escape').decode().replace('\\', '%') + '%2c' + to_
    return from_, to_


if __name__ == '__main__':
    username = input('12306登录名：')  # 12306用户名
    password = input('12306登录密码：')  # 12306密码
    order = int(input('【车次类型，从上到下1、2、3、4】:'))  # 车次选择，0代表所有车次，1表示第一行的车次，2表示第二行的车次，以此类推
    # 乘客名，比如 passengers = ['XXX', 'XXX']
    # 学生票需注明，注明方式为：passengers = ['XXX(学生)', 'XXX']
    passengers = input('乘车人【学生票输入示例：张三(学生)】,多个人用+隔开：').replace(' ', '')
    passengers = passengers.split('+')
    # 日期，格式为：'2019-01-28'
    dtime = input('乘车日期【示例：2019-01-30】：').replace(' ', '')
    while True:
        start = input('起始站【示例：北京】：').replace(' ', '')
        end = input('终到站：').replace(' ', '')
        station = get_cookie(start, end)
        if None not in station:
            break
    seat_type = input('【输入车次类型value】二等座、一等座、商务座、硬座、硬卧、软卧、动卧、高级动卧分别对应【O(大写O)、M、9、1、3、4、F、A】')
    Buy_Tickets(username, password, order, passengers, dtime, station[0], station[1]).start_buy()
