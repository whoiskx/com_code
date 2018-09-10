import pymongo
from openpyxl import load_workbook


# 本地
# conn = pymongo.MongoClient()
# urun = conn.urun
# 生产
# conn_product = pymongo.MongoClient('mongodb://120.78.237.213:27017')


def insert():
    conn_product = pymongo.MongoClient('mongodb://120.78.237.213:27017')
    article = {'name': 'hd.comment', 'domain': 'hd.comment.yunrunyuqing.com', 'main_ip': '60.190.238.166',
               'backup_ip': '120.78.237.190',
               'monitor': "http://hd.comment.yunrunyuqing.com:38010/hadoop_change_hosts.html",
               'changing': False, 'end_time': None, 'close': False}

    # urun['aliyun_dns'].insert(d)
    conn_product['taskDnsSwitch']['aliyun_dns'].insert(article)


def get_name():
    pass


def main():
    wb = load_workbook(filename='domain.xlsx', read_only=True)
    sheet = wb.active

    for index, row in enumerate(sheet.rows):
        if index == 0:
            continue
        for cell in row:
            print(cell.value)
        break


if __name__ == '__main__':
    main()
