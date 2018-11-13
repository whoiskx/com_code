# -*- coding: utf-8 -*-
from openpyxl import load_workbook, Workbook


def main():
    file_name = '汕头公安局.xlsx'
    wb = load_workbook(file_name)

    # 获取工作表
    # sheet = wb.get_sheet_names()
    sheet = wb.active

    # 获取单元格
    # 获取某个单元格的值，观察excel发现也是先字母再数字的顺序，即先列再行
    # b4 = sheet['B4']
    # cell 3个属性 row, column, coordinate
    account_list = ['SignID', 'aishangjinzao', 'chwlzch', 'xiashan_001', 'Shantou4', 'chenghaisns', 'chenhzxiang',
                    'CHXNZX0754', 'chv100 ', 'gh_54c8d6a85ac5', 'gh_194f54c5f9a2', 'D-Fashion ', 'chsq0754',
                    'chenghaiqz', 'kxtiandi ', 'chenghaiqushi', 'batou1234567891', 'chenghaif', 'CH-NEW', 'chdsj0754',
                    'csjc_LC', 'batoubbs', 'CTQAOE', 'cdzzpwvip', 'gh_7bbaa0fba604', 'cd_baihualin', 'cdwbvip',
                    'cwp348 ', 'cyzb0754', 'cyyixian', 'XCTong888', 'wx-xifengcun', 'cywsq515100', 'cyshw1688',
                    'cy515100', 'gh_30ce57d98c78', 'chaoyanglive', 'shantoudalaba', 'cymcshq', 'CYJZZXFW93 ',
                    'gh_211033224bc3', 'CYHXSHQ', 'chaoyanglive', 'qq21916', 'CCTVS01', 'youlidszx', 'gh_4274c8e8e3f7',
                    'chaoyangba', 'cssph99', 'gh_c5d23ea79e7c', 'csrzxpt?', 'chaoshanren520', 'GD-CSQ',
                    'gh_0c9c1764e0ee', 'chao6666shan ', 'CS-LTT', 'chaoiiii', 'crcscsr ', 'gh_191e435814b0',
                    'pacn0754 ', 'XC1688999', 'cnxs8888 ', 'cnwsqw168 ', 'STCN_CNR', 'chaonantai ', 'LGTV0754 ',
                    'stcnlm', 'chengtianWechat', 'cncdlm', 'cncy8888', 'chaoshan889 ', 'xilu2015', 'chaoyds',
                    'fenghuanxianzi', 'gh_2198f77baaec', 'gurao9999', 'aibang011', 'guraobang', 'gurao-BST',
                    'gh_0960eb13255e', 'grdyxc', 'gh_e122765c8f82', 'haopai8', 'gh_8e2e1b98a764', 'Guraowang',
                    'GURAOLL ', 'ugurao', 'cyzx998?', 'lovegurao', 'guraozhi', 'uuylw66', 'gurao-me', 'gh_5826fb62406a',
                    ' gurao99999 ', 'GuRaoZiXunPingTai', 'aas13808', 'tycycn', 'GuiYuRen168', 'stgysh', 'uguiyu',
                    'wxyouye', 'HJFY007', 'dahao515071 ', 'HPQ6699', 'jiazcs', 'jinrigurao', 'jinrixilu',
                    'jinzaojiaxiang', 'cytv0754', 'jzshzs168', 'jinzaoshiyixiang', 'jingdu0754', 'smg0754',
                    'liangyingren168', 'LYR-01', 'gh_59bf6935a5ae', 'gh_346323cda021', ' popst0754', 'LGQILV',
                    'xzgzs8888', 'mlch666888', 'ccyy0754', 'hjshq515071', 'iLovenanAo', 'nanaodiandi', 'na30754',
                    'nanaoxiaodaodjs', 'nanao144', 'love-st0754', 'gh_0048c34101ff', 'chenghaiwanshitong',
                    'gh_3da7c0b7d527', 'stjinri', 'stswazui', 'STweidao', 'aishantou', 'Swatowys', 'J-955555', 'tpshdq',
                    'tongyuquan168', 'ituopu', 'tpsc82522111', 'tuopxinxianshi', 'wenminggurao', 'waisharen_weixin',
                    'wz_c-h', 'whgd_me', 'woaichendian', 'gh_8fc485049716', 'XILUQUAN1', 'xiluw1688', 'xlshj1',
                    'gh_eff8efba535c', 'xs87778', 'xiashan-qing', 'xsq0536', 'xsshq2015', 'XSCATV', 'xiashanDA',
                    'gurao88888', 'xx360net', 'stsxfcn', 'yanhongrenjia', 'yanhongshenghuo', 'lhqsh0768', 'yxsh0796',
                    'IM0754', 'zsgurao', 'CNlugang', 'zsnanao', 'CNsimapu', 'tuopuu', 'STCHGA', 'gh_fac8f6b5e04c',
                    'cyxcfb ', 'STCN_CNZX', 'haojiangxuanchuan?', 'stshjq', 'gh_6b2abde26150', 'st-longhu',
                    'wsdzb0754 ', 'stslhwm', 'gh_aa29a1a37296', 'naxgqt', 'WMShanTou', 'stbjzz', 'stchedu', 'stfzjz',
                    'gh_a78ef1e3d11e', 'stjjjc', 'stsrmjcy', 'stlhgafj ', 'shantouyouth', 'shantourenshe', 'chqyjb',
                    'stszfyjb', 'l3646631', 'gh_946ba171c4f6', 'gh_eb04bcbf5738', 'stchwst', 'chrchs', 'chrm0754 ',
                    'gh_994675036163', 'cdxchenghai', 'jrch88', 'cd7222', 'cyq0661', 'cyq0754', 'cy-bbs', 'cswst8',
                    'csrm111', 'wwwchenghaicc', 'chbbscn', 'guanzhushantou', 'grt_jryx', 'hepancom', 'hbcs99',
                    'jrch20150601', 'guiyuweishenghuo', 'grt_jryx', 'J-599999', 'CH-BST', ' www_hepan_com ', 'nacsh688',
                    'weinanao114', 'stucaogenbobao', 'gh_f7c73e058c77 ', 'edaynew', 'shantoubang', 'gh_53f4bbb8d2db',
                    'stdsbxw', 'stganlantai', 'stgz0754', 'minshengdangan', 'strm0754', 'Chaoshanq', 'st-daily',
                    'wwwi754com', 'gh_23158584e0f9', 'sttqwb', 'stwst8', 'sttvnews', 'STYiXian', 'ssst201509',
                    'mldl257', 'wzshantou', 'wmch0754', 'zmcqds', 'tp-shq2', 'astp0754 ', 'loveinswatow', 'ASHM0754',
                    'hepannews', 'csbolan', 'DOU754 ', 'chyx200', 'gh_e3861a3bff9d', 'ddzxdy', 'chwl0754', 'chbtsx',
                    'gh_de35c9d4eaf5', 'chenghaiyibai', 'CDWBPT0754 ', 'gh_76a631d8d469', 'cncdq365', 'cyzx515100',
                    'cy-shb', 'cyrm0754', 'cyjz1688', 'cyhx0754', 'haimen0754', 'cygb0754', 'CYGRSHQ', 'cswhyjy',
                    'cyjp0754', 'cscstv', 'css_sty', 'jzg516538', 'gh_0f05b767e119', 'csr540 ', 'st_rainbow',
                    'ischaoshan', 'cnw515100', 'cnshq0754', 'chaonanquan', 'dshantou', 'Vchaoshan?', 'gd_st001',
                    'guraochihuo', 'guraoquan', 'guraoshequ', 'guanbu000', 'guiyushequ ', 'GYSL88', 'gywsh0813',
                    'gh_eb8321aa9824', 'wxcoupon', 'hepu515098', 'LJCS5533', 'huodongcheng520', 'jinrichaoyang',
                    'jr_zbs', 'jujiao0754', 'lhst0754?', 'gh_bd00c5c8bd05', 'st13501414036', 'nanaobest', 'nadqgw',
                    'nhan868', 'naha868', 'stnanaoly', 'Nanao_SC', 'nihaost', 'cohere', 'grshb365', 'quanqiugurao',
                    'st-chwl', 'stchihe', 'chi0754', 'is0754', 'shantoudxs', 'stualumni', 'stu_news', 'shantouhuashi',
                    'stpeople754', 'shantoutop', 'gh_e1ed414c3516', 'shantouzx', 'shantouqh', 'stouquan', 'HOT0754',
                    'shantoushequ12345678', 'stlives', 'stshjz ', 'stshiwan', 'shantouqiaolian', 'ascs99', 'istbst',
                    'hey0754', 'istwsh', 'ST07542016', 'cycy0754', 'shendu0754', 'sdst0754', 'Szchaoshang',
                    'cccsp1017 ', 'tongyuzx', 'wanbaoshantou', 'aishangst', 'cv0754、in0754', 'csrzzh', 'woaishantou1',
                    'women0754', 'xilu-ren?', 'xiluw515163', 'XiaShanTong8', 'XSweishenghuo888', 'xsdxcs', 'zsst88']
    # for row in sheet.rows:
    #     for i, cell in enumerate(row):
    #         if i == 2:
    #             print(cell.value)
    #             account_list.append(cell.value)
    print(len(account_list))


if __name__ == '__main__':
    main()
