import requests
from selenium import webdriver

def get_job():
    """发送请求获取任务"""
    return 'josn_dict'


def consumer_job(jobs=''):
    """执行并保存"""
    driver = webdriver.Chrome()
    url = 'https://www.facebook.com/701004359919966'
    driver.get(url)
    html = driver.page_source
    with open("temp.html", 'w', encoding='utf-8') as f:
        f.write(html)
    return 'OK'


def main():
    jobs = get_job()
    consumer_job(jobs)


if __name__ == '__main__':
    main()
