# -*- coding: utf-8 -*-
from openpyxl import load_workbook, Workbook


def main():
    file_name = '广州市委打标签的相关公众号.xlsx'
    wb = load_workbook(file_name)

    # 获取工作表
    # sheet = wb.get_sheet_names()
    sheet = wb.active

    # 获取单元格
    # 获取某个单元格的值，观察excel发现也是先字母再数字的顺序，即先列再行
    # b4 = sheet['B4']
    # cell 3个属性 row, column, coordinate

    account_list = []
    count = 0
    for index, row in enumerate(sheet.rows):
        if index == 0:
            continue
        for i, cell in enumerate(row):
            if i == 0:
                # print(cell.value)
                # if '\\N' in cell.value:
                #     count += 1
                #     continue
                account_list.append(cell.value)
    print((account_list))
    print(len(account_list))
    print(count)


if __name__ == '__main__':
    main()
