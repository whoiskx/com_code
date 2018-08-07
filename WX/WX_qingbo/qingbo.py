import time

from selenium import webdriver

driver = webdriver.Chrome()


url = "http://www.gsdata.cn"
driver.get(url)
time.sleep(4)
register_login = driver.find_element_by_class_name('useinfo').find_elements_by_tag_name('a')
login = register_login[1]
login.click()
time.sleep(3)
input_button = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/a[2]/img')
input_button.click()
time.sleep(2)

login_button = driver.find_element_by_xpath('//*[@id="login-form"]/div/div[1]/input')
password_button = driver.find_element_by_xpath('//*[@id="login-form"]/div/div[2]/input')

login_button.send_keys('18390553540')
password_button.send_keys('qb123258456')
button = driver.find_element_by_xpath('//*[@id="login-form"]/div/div[4]/button')
time.sleep(1)
button.click()
time.sleep(2)

search_input = driver.find_element_by_xpath('//*[@id="search_input"]')

search_input.send_keys('富翁俱乐部 ')
search_button = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/button[1]')
search_button.click()
time.sleep(2.5)

gxh = driver.find_element_by_xpath('//*[@id="nickname"]')
gxh.click()
time.sleep(2)

all_handles = driver.window_handles   #获取到当前所有的句柄,所有的句柄存放在列表当中
print(all_handles)
'''获取非最初打开页面的句柄'''
for index, handles in enumerate(all_handles):
	if index == 1:
		driver.switch_to_window(handles)

for i in range(2):
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(1)

html = driver.page_source
print(html)

data_all = driver.find_elements_by_css_selector('.wxDetail.bgff')
datas = data_all[-1]
items = datas.find_elements_by_class_name('clearfix')
for count, item in enumerate(items):
	if count == 0:
		continue
	url = item.find_element_by_tag_name('a').get_attribute('href')
	read_num = item.find_element_by_css_selector('.wxAti-info').find_element_by_tag_name('span').text
	praise_num = (item.find_element_by_css_selector('.wxAti-info').find_elements_by_tag_name('span'))[-1].text
	print(url, read_num, praise_num)

html = driver.page_source
print(html)
with open('xx.html', 'w', encoding='utf-8') as f:
	f.write(html)


import urllib.parse

def search_page(name):
	url = 'http://www.gsdata.cn/query/wx?q={}'.format(name)
	driver.get(url)
	time.sleep(4)
	html = driver.page_source
	print(html)
	print('1')


def main():
	raw_name = ''
	name = urllib.parse.quote(raw_name)
	search_page(name)


if __name__ == '__main__':
	main()