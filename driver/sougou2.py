import time

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# --no-sandbox 会导致 webdriver无法退出
# chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)
# print("get dirver")
# driver.get('https://www.baidu.com/')
# time.sleep(1)
# driver.save_screenshot('baidu.png')
# print('OK')
# driver.quit()

def crack_sougou(self, url):
    print('------开始处理未成功的URL：{}'.format(url))
    if re.search('weixin\.sogou\.com', url):
        print('------开始处理搜狗验证码------')
        self.driver.get(url)
        time.sleep(6)
        if '搜公众号' in self.driver.page_source:
            print('浏览器页面正常' + '直接返回')
            print('title{}'.format(self.driver.title))
            return
        try:
            img = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeImage')))
            print('------出现验证码页面------')
            location = img.location
            size = img.size
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            screenshot = self.driver.get_screenshot_as_png()
            screenshot = Image.open(BytesIO(screenshot))
            captcha = screenshot.crop((left, top, right, bottom))
            captcha_path = get_captcha_path()
            captcha.save(captcha_path)
            captcha_name = os.path.basename(captcha_path)
            try:
                # raise RuntimeError
                captch_input = ''
                files = {'img': (captcha_name, open(captcha_path, 'rb'), 'image/png', {})}
                res = requests.post(url=GETCAPTCHA_URL, files=files)
                res = res.json()
                if res.get('Success'):
                    captch_input = res.get('Captcha')
            except Exception as e:
                print('本地识别搜狗验证码获取异常，使用打码平台：{}'.format(e))
                with open(captcha_path, "rb") as f:
                    filebytes = f.read()
                captch_input = captch_upload_image(filebytes)
                # print('------验证码：{}------'.format(captch_input))
            print('------验证码：{}------'.format(captch_input))
            if captch_input:
                input_text = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                input_text.clear()
                input_text.send_keys(captch_input)
                submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                time.sleep(1)
                self.driver.save_screenshot("click_after.png")
                submit.click()
                time.sleep(2)
                self.driver.save_screenshot("click_before.png")
                # try:
                if '搜公众号' not in self.driver.page_source:
                    # print('当前页面{}'.format(self.driver.page_source))
                    print('搜公众号 不在页面中验证失败')
                    print('title{}'.format(self.driver.title))
                    return
                print('------验证码正确------')
                # except Exception as e:
                #     print('--22222222----验证码输入错误------ {}'.format(e))
        except Exception as e:
            print('------未跳转到验证码页面，跳转到首页，忽略------ {}'.format(e))
for i in range(30):
    driver.get('https://weixin.sogou.com/weixin?type=1&s_from=input&query=yqcc0353&ie=utf8&_sug_=n&_sug_type_=')
    if '搜公众号' not in driver.page_source:
        # print('当前页面{}'.format(self.driver.page_source))
        print('搜公众号 不在页面中验证失败')
    time.sleep(0.4)
if '搜公众号' not in driver.page_source:
    # print('当前页面{}'.format(self.driver.page_source))
    print('搜公众号 不在页面中验证失败, 截图')
    driver.save_screenshot('sougou.png')
else:
    driver.save_screenshot('sougou.png')
print('OK')