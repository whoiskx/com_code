# -*- coding: utf-8 -*-

account = ['sddxchanyeyuan', 'gh_8a970e8c2cfb', 'gh_fb30cdaa3a8c', 'hunanZDJT', 'ikejianet', 'gushizhazhi', 'gh_f27550e44f6a', 'gh_f5189da4a322', 'fjzpzjj', 'peiqidadada', 'HUAMOO2011', 'babycare_house', 'yunlty', 'gh_21ccad8ce721', 'gh_4e7dd1fd144e', 'gh_25ec121b8f38', 'gdcpqz', 'GCIG_2017', 'xrrdqggs', 'gh_63d88e5eebd3', 'Q45005959', 'NX5573', 'dmwz610', 'gh_cf2c85e52b37', 'tchongya', 'gh_6856eecb0ac7', 'mc6265287', 'gh_9865f328d1b7', 'gh_a2735af52b45', 'k-328888', 'gh_b0b3f3a1ab92', 'luyechashi', 'gh_ef4161cde0b6', 'mskt2017', 'gh_a96fb91b779c', 'name8_name', 'gh_03ba214dfd41', 'gh_233388dd0a31', 'gh_761eea6d5129', 'PEDESTRIAN___', 'gh_1f9112861625', 'c18288988', 'gh_85e983a35175', 'DanielLin118', 'gh_9e8157551721', 'huikan507', 'a13908985878', 'tingxizang', 'jinshigwy', 'gh_675ac8afde42', 'brightedu2010', 'laitbe', 'gh_4d430c521cf6', 'gh_714a37aaab7c', 'support-123', 'gh_9af0845f2907', 'gh_ce8eb7974464', 'gh_135bd2b2a869', 'yk5529', 'obsessaboutyou', 'gh_5f5046830dce', 'hnjk55', 'hhddd2011', 'hwjzxlan', 'gh_005a51b86e09', 'vsp824', 'gh_ecaa03e9165c', 'BUA-Dragon', 'ycdcxx', 'jiaxinyueyan', 'gh_3e572c898c28', 'gh_9a34119ea9f9', 'gh_b3ee23137192', 'gh_b601dc95d59a', 'xqwb321', 'gh_b209bbd18180', 'gh_81d8079e8385', 'FC_Riesling', 'dopa1199', 'zyqztb2018', 'JYTY0001']
print(len(account))
import requests
for a in account:
    url = 'http://127.0.0.1:8008/WeiXinArt/AddAccount?account={}'.format(a)
    r = requests.get(url)
    print(r.text)