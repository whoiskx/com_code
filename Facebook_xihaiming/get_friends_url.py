from setting import driver_facebook, execute_times
from pyquery import PyQuery as pq
import time
from random import randint
import re
import json



def obj_dumps(obj):
    s = json.dumps(obj, indent=2, ensure_ascii=False)
    with open('friends_url.txt', 'w', encoding='utf-8') as f:
        f.write(s)
    return s


def parse_index(html):
    url_div = re.findall(r'<div class="fsl fwb fcb">.*?</div>', html)
    results = []
    for index, url in enumerate(url_div):
        e = pq(url)
        name = e("a").text()
        link = e('a').attr("href")
        results.append({"name": name, "link": link})
    print('总共{}个好友'.format(len(results)))
    all_url = obj_dumps(results)
    return all_url


def main():
    driver = driver_facebook()
    time.sleep(2)
    driver.get(
        'https://www.facebook.com/profile.php?id=100018160331338&lst=100005036989194%3A100018160331338%3A1529916881&sk=friends&source_ref=pb_friends_tl')
    time.sleep(2)
    execute_times(driver, 70)
    html = driver.page_source

    with open("friends_all.html", 'w', encoding='utf-8') as f:
        f.write(html)
    # with open("friends_all.html", 'r', encoding='utf-8') as f:
    #     html = f.read()

    all_url = parse_index(html)


if __name__ == '__main__':
    main()

    # 小 test
    # fooo = '1'
    # def foo():
    #     # fooo += 'a'
    #     print(fooo)
    # foo()

    # def log(*args, **kwargs):
    #     time_format = '%y-%m-%d %H:%M:%S'
    #     value = time.localtime(int(time.time()))
    #     dt = time.strftime(time_format, value)
    #     with open('log.txt', 'a', encoding='utf-8') as f:
    #         print(dt, *args, file=f, **kwargs)
    # log(1)

    # from T_test_login import foo
    # foo()