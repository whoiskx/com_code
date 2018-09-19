# -*- coding: utf-8 -*-
import pymongo

from openpyxl import load_workbook, Workbook
from setting import urun

file_name = 'domain.xlsx'
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
for index, row in enumerate(sheet.rows):
    if index == 0:
        continue
    r = row
    data = {
    "name" : r[0].value,
    "domain" : r[1].value,
    "main_ip" : r[2].value.split(':')[0],
    "backup_ip" : r[3].value.split(':')[0],
    "monitor" : r[4].value,
    "changing" : False,
    "end_time" : None,
    "close" : False
}
    urun['aliyun_dns'].insert(data)
    print(data)
    # for i, cell in enumerate(row):
    #     print(cell.value)

    # break