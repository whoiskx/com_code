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

    def save_change(self, domain_detail):
        domain_detail['changing'] = True
        domain_detail['end_time'] = int(time.time())
        return domain_detail

    def swich_ip_test(self, ip, domain_detail):
        domain_detail['current_domain'] = ip
        return domain_detail

    def protect_period(self, domain_detail, now):
        change_deadline = domain_detail.get('end_time')
        if change_deadline is not None:
            time_difference = now - change_deadline
            if time_difference > 5:
                domain_detail['changing'] = False
            else:
                return None

    def run(self):
        domain_info = [{'name': 'test', 'domain': 'test.yunrunyunqing.com', 'main_ip': '61.164.49.130',
                        'backup_ip': '124.239.144.163', 'monitor': "http://test.yunrunyuqing.com:19002/test.html",
                        'changing': True, 'end_time': int(time.time()), 'close': False}]

        domain_info = [{'name': 'test', 'domain': 'test.yunrunyunqing.com', 'main_ip': '61.164.49.130',
                        'backup_ip': '124.239.144.163', 'monitor': "http://test.yunrunyuqing.com:19002/test.html",
                        'changing': False, 'end_time': None}]
        d = {'name': 'test', 'domain': 'test.yunrunyunqing.com', 'main_ip': '61.164.49.130',
             'backup_ip': '124.239.144.163', 'monitor': "http://test.yunrunyuqing.com:19002/test.html",
             'changing': False, 'end_time': None, 'current_domain': '61.164.49.130', 'close': False}

        domain_info = [d, d, d, d, ]
        error_max = 4
        while True:
            # 拿到所有域名
            # 迭代并判断故障域名
            # 修改为备用IP, 切换完成设置保护时间
            print("domain loop start")
            for domain_detail in domain_info:
                now = int(time.time())
                # 发送请求 根据响应判断服务器是否故障
                test_url = domain_detail.get('monitor')
                # url = 'http://test.yunrunyuqing.com:19002/test.html'
                # 解析出域名
                # 一
                # parsed_url = urlparse(test_url)
                # domain_port = parsed_url.netloc
                # parsed_domain = domain_port.split(':')[0]

                # 二
                domain = domain_detail.get("domain")
                # current_ip = socket.gethostbyname(parsed_domain)
                main_ip = domain_detail.get('main_ip')
                backup_ip = domain_detail.get('backup_ip')
                current_ip = domain_detail.get('current_domain')
                if current_ip == main_ip:
                    # 当前IP是主IP
                    print('当前是主IP{}'.format(current_ip))
                    changing = domain_detail.get('changing')
                    if changing is False:
                        # 确保切换主到备3分钟内没有执行修改到备用的操作
                        count = 0
                        while True:
                            try:
                                # raise RuntimeError
                                resp = requests.get(test_url)
                                if resp.status_code >= 400:
                                    # self.login()
                                    # self.swich_ip()
                                    count += 1
                                    if count == error_max:
                                        print('切换到备用IP, 当前IP{}'.format(current_ip))
                                        domain_detail = self.swich_ip_test(backup_ip, domain_detail)
                                        domain_detail = self.save_change(domain_detail)
                                        count = 0
                                        break
                                    print('server fault: code error')
                                else:
                                    break
                                print('{} normal '.format(domain))
                            except Exception as e:
                                # self.login()
                                # self.swich_ip()
                                count += 1

                                if count >= error_max:
                                    print('切换到备用IP, 当前IP{}'.format(current_ip))
                                    domain_detail = self.swich_ip_test(backup_ip, domain_detail)
                                    domain_detail = self.save_change(domain_detail)
                                    break
                                print('server fault: requests get error')
                    else:
                        # change_deadline = domain_detail.get('end_time')
                        # if change_deadline is not None:
                        #     time_difference = now - change_deadline
                        #     if time_difference > 5:
                        #         domain_detail['changing'] = False
                        #     else:
                        #         continue
                        self.protect_period(domain_detail, now)

                elif current_ip == backup_ip:
                    # 备切主 当前IP是备用服务器
                    print('当前是备用IP{}'.format(current_ip))
                    changing = domain_detail.get('changing')
                    if changing is False:
                        main_url = test_url.replace(domain, main_ip)
                        print("main_url {}".format(main_url))
                        count = 0
                        while True:
                            try:
                                resp = requests.get(main_url)
                                if resp.status_code < 400:

                                    count += 1
                                    if count >= error_max:
                                        print('切换到主IP, 当前{}'.format(current_ip))
                                        # self.login()
                                        # self.swich_ip(main_ip)
                                        domain_detail = self.swich_ip_test(main_ip, domain_detail)
                                        domain_detail = self.save_change(domain_detail)
                                        break

                                    print('server main normal')
                            except Exception as e:
                                print("backup server requests get error")
                                break

                    else:
                        # change_deadline = domain_detail.get('end_time')
                        # if change_deadline is not None:
                        #     time_difference = now - change_deadline
                        #     if time_difference > 5:
                        #         domain_detail['changing'] = False
                        #     else:
                        #         continue
                        self.protect_period(domain_detail, now)
            time.sleep(5)
            print("domain loop over")
            # break


if __name__ == '__main__':
    test = IpSwith()
    test.run()
