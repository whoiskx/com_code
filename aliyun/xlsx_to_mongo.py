# -*- coding: utf-8 -*-
import pymongo

from openpyxl import load_workbook, Workbook
# from setting import urun

file_name = 'domain_new.xlsx'
# 打开 默认可读写
wb = load_workbook(file_name)

# 获取工作表
# sheet = wb.get_sheet_names()
sheet = wb.active

# 获取单元格
# 获取某个单元格的值，观察excel发现也是先字母再数字的顺序，即先列再行
# b4 = sheet['B4']
# cell 3个属性 row, column, coordinate
conn = pymongo.MongoClient('mongodb://120.78.237.213:27017')
urun = conn.taskDnsSwitch


def check():
    names = []

    for index, row in enumerate(sheet.rows):
        if index == 0:
            continue
        r = row
        data = {
            "name": r[0].value,
            "domain": r[1].value,
            "main_ip": r[1].value.split(':')[0],
            "backup_ip": r[2].value.split(':')[0],
            "monitor": r[3].value,
            "changing": False,
            "end_time": None,
            "close": False
        }
        # urun['aliyun_dns'].insert(data)
        # 检测是否一致
        for instance in urun['aliyun_dns'].find():

            if instance.get('name') == data.get('name'):
                if instance.get('main_ip') == data.get('main_ip') and instance.get('backup_ip') == data.get(
                        'backup_ip') and instance.get('monitor') == data.get('monitor') and instance.get(
                        'domain') in data.get('monitor'):
                    names.append(data.get('name'))
                    print('相等', instance.get('name'))
                else:
                    print(instance, data, '不相等')
        print('11')
    print(names)
    # for i, cell in enumerate(row):
    #     print(cell.value)

    # break

def update():
    names = ['热门微博', '微博博主信息', '微信公众号', '新闻APP', '文章评论', '全局境外社交', '全局文章接口', '全局文章外语接口', '全局文章折叠话题', '全局微博', '全局微信']
    for index, row in enumerate(sheet.rows):
        if index == 0:
            continue
        r = row
        data = {
            "name": r[0].value,
            # "domain": r[1].value,
            # "main_ip": r[1].value.split(':')[0],
            # "backup_ip": r[2].value.split(':')[0],
            "monitor": r[3].value,
            # "changing": False,
            # "end_time": None,
            # "close": False
        }
        # urun['aliyun_dns'].insert(data)
        # 检测是否一致
        for instance in urun['aliyun_dns'].find():

            if instance.get('name') == data.get('name'):
                urun['aliyun_dns'].update({'name':instance.get('name')}, {'$set':{'monitor': data.get('monitor')}})
                print('更新成功', instance.get('name'))
        print('11')

def main():
    # check()
    update()
if __name__ == '__main__':
    main()
