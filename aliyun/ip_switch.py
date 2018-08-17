from datetime import datetime
import time
import requests
from selenium import webdriver
from urllib.parse import urlparse
import socket


class IpSwith(object):
    def __init__(self):
        self.driver = None

    def login(self):
        if self.driver is None:
            self.driver = webdriver.Chrome()
        url = 'https://signin.aliyun.com/1604195877004448/login.htm?callback=https%3A%2F%2Fdns.console.aliyun.com%2F'
        self.driver.get(url)
        time.sleep(1)
        login_name = self.driver.find_element_by_xpath('//*[@id="user_principal_name"]')
        time.sleep(1)
        login_name.clear()
        login_name.send_keys('domain@1604195877004448')
        next_step = self.driver.find_element_by_xpath('//*[@id="J_FormNext"]/span')
        next_step.click()
        login_passwd = self.driver.find_element_by_xpath('//*[@id="password_ims"]')
        time.sleep(0.5)
        login_passwd.send_keys('yunrun!@#123')
        time.sleep(1)
        button = self.driver.find_element_by_xpath('//*[@id="u22"]/input')
        button.click()
        time.sleep(1)
        # 登录完成

    def swich_ip(self, ip):
        # 进入阿里云
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/i[1]').click()
        time.sleep(3)
        domin_yun = self.driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[3]/td[2]/span[2]/div[1]/a')
        domin_yun.click()
        time.sleep(2)

        change_button = self.driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[9]/span/span[1]')
        change_button.click()

        # 清空并输入新IP
        ip_input = self.driver.find_element_by_xpath('//*[@id="value"]')
        ip_input.clear()
        #    ip_input.send_keys('1.1.1.1')
        ip_input.send_keys(ip)
        time.sleep(0.5)
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[1]/div[3]/div/button[2]').click()
        time.sleep(50)
        self.driver.quit()

    def domain_to_ip(self, domain):
        ip = socket.gethostbyname(domain)
        return ip

    def save_change(self, domain_detail):
        domain_detail['is_change'] = True
        domain_detail['end_time'] = int(time.time())
        return domain_detail

    def run(self):
        domain_list = [{'name': 'test', 'domain': 'test.yunrunyunqing.com', 'main_ip': '61.164.49.130',
                        'backup_ip': '124.239.144.163', 'monitor': "http://test.yunrunyuqing.com:19002/test.html",
                        'is_change': True, 'end_time': int(time.time())}]

        domain_list = [{'name': 'test', 'domain': 'test.yunrunyunqing.com', 'main_ip': '61.164.49.130',
                        'backup_ip': '124.239.144.163', 'monitor': "http://test.yunrunyuqing.com:19002/test.html",
                        'is_change': False, 'end_time': None}]
        d = {'name': 'test', 'domain': 'test.yunrunyunqing.com', 'main_ip': '61.164.49.130',
         'backup_ip': '124.239.144.163', 'monitor': "http://test.yunrunyuqing.com:19002/test.html",
         'is_change': False, 'end_time': None}

        domain_list = [d, d, d, d]
        while True:
            # 拿到所有域名
            # 迭代并判断故障域名
            # 修改为备用IP, 切换完成设置保护时间
            for domain_detail in domain_list:
                now = int(time.time())
                test_url = domain_detail.get('monitor')
                # url = 'http://test.yunrunyuqing.com:19002/test.html'
                parsed_url = urlparse(test_url)
                domain_port = parsed_url.netloc
                parsed_domain = domain_port.split(':')[0]

                current_ip = self.domain_to_ip(parsed_domain)
                main_ip = domain_detail.get('main_ip')

                if current_ip == main_ip:
                    is_change = domain_detail.get('is_change')
                    if not is_change:
                        # 确保修主到备3分钟内没有执行修改到备用的操作
                        try:
                            # resp = requests.get(test_url)
                            resp.status_code = 406
                            if resp.status_code >= 400:
                                # self.login()
                                # self.swich_ip()
                                self.save_change(domain_detail)
                                print('server fault: code error')
                            print('server normal')
                        except Exception as e:
                            # self.login()
                            # self.swich_ip()
                            self.save_change(domain_detail)
                            print('server fault: request error')

                    else:
                        change_deadline = domain_detail.get('end_time')
                        if change_deadline is not None:
                            time_difference = now - change_deadline
                            if time_difference > 5:
                                domain_detail['is_change'] = False
                            else:
                                continue
                                # break



                else:
                    # 判断备用服务器
                    # 怎么知道主IP是好的？？
                    resp = requests.get(test_url)
                    if resp.status_code >= 400:
                        # self.login()
                        # self.swich_ip()
                        print('server fault')
                        pass

            # url = 'http://test.yunrunyuqing.com:19002/test.html'
            # main_url = 'http://61.164.49.130:19002/test.html'
            # backup_url = 'http://124.239.144.163:19002/test.html'
            # ip = {
            #     'main': '61.164.49.130',
            #     'back_up': '124.239.144.163'
            # }
            count = 0
            try:
                resp = requests.get(url)
                print(resp.status_code)
                count = 0
            except Exception as e:
                if count == 3:
                    # self.login()
                    # self.swich_ip(ip.get('back_up'))
                    time.sleep(100)
                count += 1

            # if resp.status_code > 400:
            #     r2 = requests.get(url)
            #     print(resp.status_code)
            #     time.sleep(1)
            #     r3 = requests.get(url)
            #     time.sleep(1)
            #     print(resp.status_code)
            #
            #     if r2.status_code > 400 and r3.status_code > 400:
            #         login_and_swich_ip(ip.get('back_up'))

            # time.sleep(60)


if __name__ == '__main__':
    test = IpSwith()
    test.run()
