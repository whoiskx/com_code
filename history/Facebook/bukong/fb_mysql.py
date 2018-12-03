import pymysql

MYSQL_HOST = '47.52.190.138'

MYSQL_PORT = 8002
MYSQL_USER = 'yunrun'
MYSQL_PASSWORD = 'Yunrun2015!@#'
MYSQL_DATABASE = 'weibotask'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'db': MYSQL_DATABASE,
    'passwd': MYSQL_PASSWORD
}

# db = pymysql.connect(**config_mysql)
# cursor = db.cursor()
# print(1)

from setting import cursor, urun
import openpyxl
from openpyxl import load_workbook, Workbook
file_name = '中美贸易（推特用户）_翠仙2018-8-9.xlsx.xlsx'
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
        print(cell.value)

        if i == 0:
            name = cell.value
        if i == 1:
            url = cell.value
    account = {
        "name": name,
        'url': url,
    }
    urun["fb_bukong"].insert(account)
#     all.append(account)
#     if index == 5:
#         break
#
# print(account)
# print(all)