#encoding=utf-8

import requests
import time


def get_txb():
    url = "https://data.wxb.com/searchResult?kw=%E8%A7%86%E8%A7%89%E5%BF%97&page=1 "
    header = {'Host': 'data.wxb.com', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Referer': 'https://account.wxb.com/?from=https%3A%2F%2Fdata.wxb.com%2FsearchResult%3Fkw%3D%25E8%25A7%2586%25E8%25A7%2589%25E5%25BF%2597%26page%3D1',
              'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.8',
              'Cookie': 'visit-wxb-id=7c5736cc99cda0e635c8958831967045; PHPSESSID=8hvca5bejg47la3q10q96rsjm3; wxb_fp_id=3774451913; Hm_lvt_5859c7e2fd49a1739a0b0f5a28532d91=1528359684'}

    cookie = {'visit-wxb-id': '7c5736cc99cda0e635c8958831967045', 'PHPSESSID': '8hvca5bejg47la3q10q96rsjm3',
              'wxb_fp_id': '3774451913', 'Hm_lvt_5859c7e2fd49a1739a0b0f5a28532d91': '1528359684',
              'Hm_lpvt_5859c7e2fd49a1739a0b0f5a28532d91': '1528360627'}

    print("begin", time.strftime("%M:%S", time.localtime()))
    # for i in range(40):
    i = 1
    while True:
        r = requests.get(url, headers=header)
        with open("log.txt", 'a') as f:
            value = time.strftime("%H:%M", time.localtime())
            print("time:{} count: {}  status: {}".format(value, i, r.status_code,), file=f)
        i += 1
        time.sleep(0.5)
        # if time.strftime("%H:%M", time.localtime()) == '12:59':
        #     break

    print("end", time.strftime("%H:%M", time.localtime()))

    r = requests.get(url, headers=header)
    print(r.text)


if __name__ == '__main__':
    get_txb()
