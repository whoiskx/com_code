from selenium import webdriver
import time

driver=webdriver.Chrome()
driver.get('http://www.baidu.com')#进入百度首页
driver.maximize_window()#窗口最大化
time.sleep(1)
driver.set_window_size(480,600)#窗口大小变化
time.sleep(1)
driver.maximize_window()
time.sleep(1)
driver.set_window_size(500,700)
time.sleep(1)
driver.maximize_window()
time.sleep(1)
driver.set_window_size(600,800)
time.sleep(1)
driver.maximize_window()
time.sleep(1)
driver.set_window_size(700,1000)
print('#窗口大小变化结束')
time.sleep(2)
driver.find_element_by_id('kw').send_keys('selenium')#输入关键字selenium
time.sleep(1)
driver.find_element_by_id('su').click()#进入selenium页面
time.sleep(3)
driver.find_element_by_xpath("//*[@id='1']/h3/a").click()
print('进入selenium官网')
time.sleep(3)
driver.find_element_by_link_text('功能自动化测试工具——Selenium篇').click()#通过锚文本定位
time.sleep(10)
windows=driver.window_handles
driver.switch_to_window(windows[1])#切换窗口

#driver.refresh()
driver.maximize_window()
time.sleep(2)
driver.close()
windows=driver.window_handles
driver.switch_to_window(windows[1])#切换窗口
time.sleep(2)
driver.close()
windows=driver.window_handles
driver.switch_to_window(windows[0])#切换窗口
content=driver.find_element_by_xpath("//*[@id='1']/div[2]").text#打印出这一部分的内容
print( content)
driver.back()
print('返回到百度首页')
time.sleep(2)
driver.forward()
print('进入下一页')
time.sleep(5)
driver.find_element_by_xpath("//*[@id='u']/a[2]").click()
driver.find_element_by_xpath("//*[@id='wrapper']/div[4]/a[1]").click()#处理有下拉框的元素
time.sleep(1)
driver.find_element_by_xpath("//*[@id='gxszButton']/a[1]").click()
time.sleep(1)
driver.switch_to_alert().accept()#处理警告弹窗
time.sleep(2)
print('处理好警告弹窗')
js="var q=document.documentElement.scrollTop=10000"
driver.execute_script(js)#处理右侧的滚动条
time.sleep(3)
print("右侧的滚动条拉倒最低处")
driver.close()