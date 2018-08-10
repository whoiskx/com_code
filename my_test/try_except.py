try:

    try:
        raise 1 == 2
    except Exception as e:
        print(e)
        # print(str(e))
        print(type(e))
        raise 1 == 2
except Exception as e:
    print(e)


def switch_tab(self, num):
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver = self.driver
    handles = driver.window_handles           # 获取当前窗口句柄集合（列表类型）
    driver.switch_to.window(handles[num-1])