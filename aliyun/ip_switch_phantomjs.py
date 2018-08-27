import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import socket
import pymongo

produce_env = True
develop_env = False
# if produce_env:
# conn = pymongo.MongoClient()
# urun = conn.urun
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# web_driver = webdriver.Chrome(chrome_options=chrome_options)
# web_driver = webdriver.Chrome

# if develop_env:

conn = pymongo.MongoClient('mongodb://120.78.237.213:27017')
urun = conn.taskDnsSwitch
# web_driver = webdriver.PhantomJS


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    # if '12:49:4' or '12:49:5' in dt:
    #     with open('log.txt', 'w', encoding='utf-8') as f:
    #         f.truncate()
    print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


class IpSwith(object):
    def __init__(self):
        self.driver = None

    def login(self):
        if self.driver:
            self.driver.quit()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--no-sandbox")
        web_driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver = web_driver
        # web_driver = webdriver.Chrome
        # web_driver = webdriver.PhantomJS
        # self.driver = web_driver()
        # self.driver.set_window_size(1920, 1080)
        # self.driver.maximize_window()


        # self.driver = webdriver.Chrome()
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
        log('登录成功')
        # 登录完成

    def swich_ip(self, ip, domain):
        # 进入阿里云
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/i[1]').click()
        time.sleep(3)
        # 进入域名管理页面
        # domin_yun = self.driver.find_element_by_xpath(
        #     '//*[@id="container"]/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[3]/td[2]/span[2]/div[1]/a')
        # domin_yun.click()
        self.driver.find_elements_by_class_name("ant-table-row")[2].find_element_by_tag_name('a').click()
        time.sleep(2)
        # 选择显示100页
        self.driver.find_element_by_class_name('ant-select-selection__rendered').click()
        choice = self.driver.find_elements_by_class_name('ant-select-dropdown-menu-item')
        choice[-1].click()
        time.sleep(1)
        # 匹配域名
        records_info = self.driver.find_elements_by_class_name('ant-table-row')
        for record in records_info:
            domain_aliyun = record.find_elements_by_class_name('ant-table-column-has-filters')[1].text

            if domain_aliyun == domain.replace('.yunrunyuqing.com', ''):
                change_div = record.find_element_by_class_name('_3VmUbwgp')
                change_div.click()
                time.sleep(1)
                # 更改IP
                ip_input = self.driver.find_element_by_xpath('//*[@id="value"]')
                ip_input.clear()
                #    ip_input.send_keys('1.1.1.1')
                ip_input.send_keys(ip)
                time.sleep(0.5)
                # self.driver.find_element_by_xpath(
                #     '/html/body/div[5]/div/div[2]/div/div[1]/div[3]/div/button[2]').click()
                time.sleep(3)
                self.driver.quit()
                return None
        log('warning 未能匹配域名')
        self.driver.quit()

    def save_change(self, domain_detail):
        domain_detail['changing'] = True
        domain_detail['end_time'] = int(time.time())
        domain = domain_detail.get("domain")
        urun['aliyun_dns'].update({'domain': domain}, {'$set': {'changing': True, 'end_time': int(time.time())}})
        return domain_detail

    def protect_period(self, domain_detail, now):
        # 主到备 10分钟内禁止再次修改
        change_deadline = domain_detail.get('end_time')
        if change_deadline is not None:
            time_difference = now - change_deadline
            if time_difference > 620:
                log("not in  protect period")
                domain_detail['changing'] = False
                urun['aliyun_dns'].update({'domain': domain_detail.get('domain')},
                                          {'$set': {'changing': False}})
            else:
                log("in protect period", time_difference)

    def backup_server_status(self, monitor_url, domain, backup_ip):
        # 判断备用服务器是否OK
        backup_url = monitor_url.replace(domain, backup_ip)
        log("backup_ip {}".format(backup_ip))
        try:
            resp = requests.get(backup_url)
            if resp.status_code >= 400:
                log("backup server error1")
                return False
        except Exception as e:
            log("backup server error2")
            return False
        return True

    def run(self):
        error_max = 4
        test_main = 0
        while True:
            # 拿到所有域名
            # 迭代并判断故障域名
            # 修改为备用IP, 切换完成设置保护时间
            start = int(time.time())
            log("domain loop start")
            for domain_detail in urun['aliyun_dns'].find():
                # 关闭域名检测
                if domain_detail.get('close') is True:
                    continue
                name = domain_detail.get('name')
                log("start test {}".format(name))
                now = int(time.time())
                # 发送请求 根据响应判断服务器是否故障
                monitor_url = domain_detail.get('monitor')
                domain = domain_detail.get("domain")
                current_ip = socket.gethostbyname(domain)
                main_ip = domain_detail.get('main_ip')
                backup_ip = domain_detail.get('backup_ip')
                if current_ip == main_ip:
                    # 当前IP是主IP
                    log('当前运行{} 主IP{}'.format(name, current_ip))
                    changing = domain_detail.get('changing')
                    if changing is False:
                        count = 0
                        while True:
                            try:
                                test_main += 1
                                if test_main <= 50:
                                    # if name == 'test':
                                    raise RuntimeError
                                resp = requests.get(monitor_url)
                                if resp.status_code < 400:
                                    break
                                if resp.status_code >= 400:
                                    count += 1
                                    if count >= error_max:
                                        status = self.backup_server_status(monitor_url, domain, backup_ip)
                                        if status:
                                            log('切换到备用IP, 当前IP{}'.format(current_ip))
                                            try:
                                                self.login()
                                                self.swich_ip(backup_ip, domain)
                                                self.save_change(domain_detail)
                                                log('切换成功')
                                            except Exception as e:
                                                if self.driver:
                                                    self.driver.quit()
                                                log('切换失败', e)
                                            break
                                    log('server fault: status code over 400')
                                else:
                                    break
                                log('{} normal '.format(domain))
                            except Exception as e:
                                log('requests', e)
                                count += 1

                                if count >= error_max:
                                    status = self.backup_server_status(monitor_url, domain, backup_ip)
                                    if status:
                                        log('切换到备用IP, 当前IP{}'.format(current_ip))
                                        try:
                                            self.login()
                                            self.swich_ip(backup_ip, domain)
                                            self.save_change(domain_detail)
                                            log('切换成功')
                                        except Exception as e:
                                            if self.driver:
                                                self.driver.quit()
                                            log('切换失败', e)
                                        break
                                log('server fault: requests get error')
                    else:
                        self.protect_period(domain_detail, now)

                elif current_ip == backup_ip:
                    # 备切主 当前IP是备用服务器
                    log('当前运行{}, 备用IP{}'.format(name, current_ip))
                    changing = domain_detail.get('changing')
                    if changing is False:
                        main_url = monitor_url.replace(domain, main_ip)
                        log("main_url {}".format(main_url))
                        count = 0
                        while True:
                            try:
                                resp = requests.get(main_url)
                                if resp.status_code < 400:

                                    count += 1
                                    if count >= error_max:
                                        log('切换到主IP, 当前IP {}'.format(current_ip))
                                        try:
                                            self.login()
                                            self.swich_ip(main_ip, domain)
                                            self.save_change(domain_detail)
                                            log('切换成功')
                                        except Exception as e:
                                            if self.driver:
                                                self.driver.quit()
                                            log('切换失败', e)
                                        break
                                    log('server main normal')
                            except Exception as e:
                                log("backup server requests get error", e)
                                break
                    else:
                        self.protect_period(domain_detail, now)
            end = int(time.time())
            log("domain loop over", (end - start))

            time.sleep(5)
            # break


if __name__ == '__main__':
    test = IpSwith()
    test.run()

    # 测试未匹配到域名 driver 正常退出
    # test.login()
    # test.swich_ip('0.0.0.0', 'sdafasdfa')
