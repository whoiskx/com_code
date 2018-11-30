# -*- coding: utf-8 -*-
import pymssql

import pymysql
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
            if i == 1 and cell.value.isdigit():
                # print(cell.value)
                # if '\\N' in cell.value:
                #     count += 1
                #     continue
                account_list.append(cell.value)
    print((account_list))
    print(len(account_list))
    print(count)


if __name__ == '__main__':
    # main()
    _id_list = ['53543625', '67486230', '61538307', '51239848', '51933582', '86308499', '65939125', '68148218', '64402046', '52621703', '52280313', '51313272', '103602785', '51239893', '124209819', '65431921', '67952974', '51076566', '51313690', '52426887', '51701320', '52817408', '65431965', '67630784', '50449190', '110930386', '51527952', '52879220', '52155431', '114956738', '51239851', '51701275', '110776439', '125042893', '103487432', '51527950', '51528122', '52777528', '51700880', '68189968', '65871705', '111068872', '51527791', '123607437', '123607472', '123607495', '50537206', '67296462', '65431961', '83182274', '51528010', '51972522', '67429222', '80219200', '55249281', '53954803', '54404240', '50956308', '67539488', '52426907', '65870280', '68268756', '79289292', '115502831', '51939866', '51021385', '67936045', '51066007', '51239855', '51510771', '58996913', '65431968', '68217964', '59716436', '59716558', '51076558', '65685896', '51631418', '51239927', '65431957', '51441352', '53667739', '50174028', '122181733', '52280318', '51240081', '66200466', '101465652', '51700882', '51701105', '67839221', '66583224', '53880761', '124734938', '68293502', '51076054', '79301274', '91133738', '103500785', '57997356', '67011851', '65573708', '68292459', '66695046', '67782068', '79386790', '107706885', '67964235', '67413527', '57997089', '66402167', '124577832', '124538288', '53005200', '123607450', '51701110', '55938332', '50495864', '59151998', '51510510', '50604088', '65399704', '51700872', '118618375', '65591765', '124235549', '66944568', '67711753', '103604000', '54305091', '115531540', '119133005', '116172773', '67967490', '51548132', '114614885', '52247587', '124345572', '110663068', '68371527', '59666374', '124260935', '65506663', '124942717', '98491073', '115921355', '65172775', '124901059', '89883649', '51239931', '51263612', '66583210', '59716437', '67130426', '65158725', '50812475', '52244040', '57997105', '51021256', '124620651', '66007559', '125088480', '67032516', '50812481', '120262647', '52777467', '51700881', '124634012', '52231993', '100365662', '124907317', '50812474', '51076560', '51076609', '54306855', '51239898', '64502399', '124394078', '51595089', '67757207', '53543521', '67257286', '66412502', '52666439', '51595043', '50977568', '50977618', '53856922', '51076562', '51701108', '125129545', '59275601', '51021248', '50977520', '50977619', '53857322', '51239934', '51701325', '53954862', '59261253', '66623843', '68350256', '114601714', '50977449', '124548023', '68157924', '123469130', '67965131', '50565620', '92423522', '57997098', '50608042', '52645863', '50977453', '52796478', '66487385', '124697115', '51528126', '53651040', '65573706', '50977524', '50977694', '50812545', '67286237', '59534620', '64933152', '64517305', '52238067', '114553904', '123394122', '50977571', '51239857', '54626152', '65431918', '52596163', '67983852', '114583707', '57409153', '51897980', '64920177', '53528157', '51527823', '64588802', '51239845', '67559441', '89261038', '107609315', '124519596', '51527822', '64855846', '123607497', '114956735', '52777479', '67239001', '65431920', '59710548', '66292237', '59709646', '67837250', '88880759', '125324772', '53647541', '67910559', '51021284', '50977491', '80253583', '68049349', '66097117', '52077209', '57106923', '65720791', '65555217', '67092436', '58078667', '115754693', '65236620', '67795219', '103534369', '50977738', '52568794', '66732672', '88299579', '54220227', '123607444', '51595091', '124577928', '58301372', '50977488', '50977493', '50977632', '53856464', '65904989', '115056900', '50977746', '80927649', '97726520', '50977839', '121793622', '64832136', '108031308', '67726825', '68077310', '54628779', '125180828', '67989703', '53651144', '59716364', '50947271', '66423278', '124982240', '124505544', '59712073', '51595483', '115341260', '50977487', '50977489', '50977748', '118419037', '52255911', '67363587', '53880976', '53881122', '103607668', '64960162', '115372935', '50812471', '52777523', '65429722', '50635635', '67867918', '107741334', '52783971', '109659255', '65720784', '50977527', '50977736', '50977755', '52403782', '58293054', '50977634', '50977686', '124701064', '52201455', '66204053', '51897755', '51055229', '51252678', '114864590', '67829720', '110983025', '65431960', '67613122', '68089988', '50977691', '50977743', '54249142', '67961043', '50977569', '50977688', '53865377', '90601974', '67092435', '67705621', '115414652', '54360473', '88015956', '64558010', '124300514', '58078678', '58078680', '50977448', '124745276', '50977750', '51897662', '66907676', '66206512', '58967536', '64826652', '51021252', '51709666', '52107676', '65798305', '59653962', '68178359', '67763499', '64868822', '91343225', '50977519', '50977893', '52254207', '124547222', '67786400', '67100000', '65934345', '68005175', '82205923', '124700825', '63672669', '65109010', '50977889', '52846994', '55736042', '80943765', '114864544', '50977525', '82301107', '67846574', '94182224', '65877445', '107644887', '68128301', '91688871', '66583225', '50829421', '64490153', '107735952', '65069398', '52568858', '68116491', '52260707', '50977490', '50977844', '65156574', '118094011', '65407785', '125024742', '50977798', '65156573', '67817819', '66292244', '67257285', '67710855', '68213196', '50701711', '124465423', '64536202', '50977625', '54310231', '50505082', '107623230', '85599493', '123896060', '61695298', '65565426', '123607435', '52248207', '123298375', '65158352', '124892730', '86077671', '51240000', '80959290', '53692168', '51510765', '53856454', '58290550', '113890702', '57179802', '53632762', '58278437', '50970461', '52299078', '54613330', '51390169', '51390173', '50972978', '53339625', '51159454', '58434922', '52881323', '52803572', '2936022', '2936022']
    from config import get_mysql_old
    account_list = []
    for _id in _id_list:
        sql = '''   
                        SELECT * FROM WXAccount where id=%s
                '''

        try:
            config_mysql = get_mysql_old()
            db = pymssql.connect(**config_mysql)
            # print('链接成功')
            cursor = db.cursor()
            cursor.execute(sql, (_id,))
            result = cursor.fetchone()
            account_list.append(result[2])
            print(result[2])
            # cursor.close()
            # db.close()
            # break
        except Exception as e:
            print('数据库上传错误 {}'.format(e))
        # break
    print(account_list)