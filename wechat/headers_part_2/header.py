# -*- coding: utf-8 -*-
import pymssql

from config import get_mysql_old


def main():
    mysql_config = get_mysql_old()
    db = pymssql.connect(**mysql_config)
    cursor = db.cursor()
    sql_select = """
            select * from wxaccount where id >70000000 order by id asc  
    """
    cursor.execute(sql_select)
    result = cursor.fetchmany(10)
    print(list(result))


if __name__ == '__main__':
    main()
