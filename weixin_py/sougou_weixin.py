import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from setting import log
url = 'https://weixin.sogou.com/'


def main():
    driver = webdriver.Chrome()
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchbox')))
    search = driver.find_element_by_xpath('//*[@id="query"]')
    search.send_keys('人民日报评论')
    time.sleep(0.5)
    search_button = driver.find_element_by_xpath('//*[@id="searchForm"]/div/input[4]')
    search_button.click()

    public_link = driver.find_element_by_xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/em')
    public_link.click()

    handles = driver.window_handles
    if len(handles) > 2:
        log('error')
    driver.switch_to.window(handles[-1])

    # info_list = driver.find_elements_by_class_name('weui_msg_card')
    # for info in info_list:
    #     title = info.find_element_by_class_name('weui_media_title')
    #     print(title)

    info_list = driver.find_elements_by_class_name('weui_media_box')
    for info in info_list:
        article_url = 'https://mp.weixin.qq.com/' + info.find_element_by_class_name('weui_media_title').get_attribute("hrefs")
        title = info.find_element_by_class_name('weui_media_title')
        print(title.text)




if __name__ == '__main__':
    main()