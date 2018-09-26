# -*- coding: utf-8 -*-
import datetime
from ftplib import FTP
import uuid
import zipfile

def main():
    ftp = FTP()  # 设置变量

    ftp.connect("110.249.163.246", 21)  # 连接的ftp sever和端口

    ftp.login("dc5", "qwer$#@!")  # 连接的用户名，密码如果匿名登录则用空串代替即可

    # zf = zipfile.ZipFile('4041070c-bd83-11e8-af9f-fc017c3bd1b0.zip', 'r')
    print('creating archive')
    # zf = zipfile.ZipFile('{}.zip'.format(str(uuid.uuid1())), mode='w')
    # try:
    #     print('adding readme.txt')
    #     zf.write('text.xml')
    # finally:
    #     print('closing')
    #     zf.close()

    # filepath = datetime.datetime.now().strftime("%Y%m%d")
    filepath = '20180926'
    # filename = uuid.uuid1()
    filename = '37eadc0a-c160-11e8-8b1e-fc017c3bd1b0.zip'
    cmd = 'STOR /{}/{}'.format(filepath, filename)

    ftp.storbinary(cmd, open(filename, 'rb'))
    print('end')


if __name__ == '__main__':
    # for i in range(10):

        main()
