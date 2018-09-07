# -*- coding: utf-8 -*-

with open('ids.txt', 'r', encoding='utf-8') as f:
    name_all = f.read()
id_list = name_all.split("\n")
print(id_list)
