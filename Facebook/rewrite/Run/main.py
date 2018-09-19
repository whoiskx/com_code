from selenium import webdriver
from choice import login_must, link_error, person, group
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(url):
    driver = webdriver.Chrome()
    driver.get(url)
    choice = ''
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'inputtext')))
    try:
        # 需要登录 https://www.facebook.com/joseph.zen.52
        driver.find_element_by_css_selector('._2nlw._2nlv')
        choice = login_must
    except Exception as e:
        pass

    try:
        # 连接错误 https://www.facebook.com/scleung.itvoice2012
        driver.find_element_by_css_selector('._4-dp')
        choice = link_error
    except Exception as e:
        pass

    try:
        # 个人
        driver.find_element_by_css_selector('._2i5e')
        choice = person
    except Exception as e:
        pass

    try:
        # 群组 https://www.facebook.com/theeclecticsbasement/
        driver.find_element_by_css_selector('._64-f')
        choice = group
    except Exception as e:
        pass

    if choice != '':
        print(choice)
        choice(driver)


if __name__ == '__main__':
    # 地方性商家
    url = 'https://www.facebook.com/pages/%E8%81%96%E5%A3%AB%E6%8F%90%E5%8F%8D%E7%81%A3%E6%B3%B3%E7%81%98/143105012420920?rf=313544202035563'
    url = 'https://www.facebook.com/pages/International-Baptist-Church-of-Manila/196088797103440?rf=214379858603733'
    url = 'https://www.facebook.com/pages/Shatin-Inn%E6%B2%99%E7%94%B0%E8%8C%B5%E9%A4%90%E5%BB%B3/362695797132037?rf=102294283185641'

    # 群组
    # https://www.facebook.com/107597712639350
    url = "https://www.facebook.com/CityHospitalBd/?rf=523780141030593"
    # 点赞评论很多
    url = 'https://www.facebook.com/AeroportoLisboa/?rf=107597712639350'

    main(url)
