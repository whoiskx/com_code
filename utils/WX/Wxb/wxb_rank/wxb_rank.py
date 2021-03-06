
import requests
import time
from pyquery import PyQuery as pq


def get_rank():

    for i in range(40, 51):
        url = "https://data.wxb.com/rank?category=21&page={}".format(i)
        header = {'Host': 'data.wxb.com', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer': 'https://account.wxb.com/?from=https%3A%2F%2Fdata.wxb.com%2FsearchResult%3Fkw%3D%25E8%25A7%2586%25E8%25A7%2589%25E5%25BF%2597%26page%3D1',
                  'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Cookie': 'visit-wxb-id=7c5736cc99cda0e635c8958831967045; PHPSESSID=8hvca5bejg47la3q10q96rsjm3; wxb_fp_id=3774451913; Hm_lvt_5859c7e2fd49a1739a0b0f5a28532d91=1528359684'}
        resp = requests.get(url, headers=header)
        print(i, resp.status_code)
        e = pq(resp.text)
        title_list = e(".wxb-avatar-subtitle").text()
        title_list2 =title_list.split()

        all_title = []
        for title in title_list2:
            with open("temp.txt", 'a') as f:
                account = title + "\n"
                all_title.append(account)
                f.write(account)

        print(all_title)
        time.sleep(2)


def _main():
    get_rank()


if __name__ == '__main__':
    _main()