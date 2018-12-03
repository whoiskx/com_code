import pymysql
from setting import cursor, urun
import openpyxl
from openpyxl import load_workbook, Workbook


file_name = '中美贸易（脸谱用户）_翠仙2018-8-9.xlsx.xlsx'
wb = load_workbook(file_name)

# 获取工作表
# sheet = wb.get_sheet_names()
sheet = wb.active

# 获取单元格
# 获取某个单元格的值，观察excel发现也是先字母再数字的顺序，即先列再行
# b4 = sheet['B4']
# cell 3个属性 row, column, coordinate
all = []
for index, row in enumerate(sheet.rows):
    if index == 0:
        continue
    name, url = '', ''
    for i, cell in enumerate(row):
        # print(cell.value)

        if i == 1:
            name = cell.value
        if i == 2:
            url = cell.value
    account = {
        "name": name,
        'url': url,
    }
    print(account)

    urun["bukong_fbbb"].insert(account)
#     all.append(account)
#     if index == 5:
#     break
#
# print(account)
# print(all)