ftp_info = None
for page_count, url in enumerate(urls_article):
    # ftp包
    ftp_info = Ftp(entity)
    name_xml = ftp_info.hash_md5(ftp_info.url)
    # with open('ftp/{}'.format(name_xml), 'w', encoding='utf-8') as f:
    self.create_xml(ftp_info.ftp_dict(), name_xml)
    ftp_list.append(name_xml)


zf_name = str(uuid.uuid1()) + '.zip'
    with zipfile.ZipFile('ftp/{}'.format(zf_name), mode='w') as zf:
        zf_comment = ftp_info.ftp_note()
        zf.comment = str(zf_comment).encode('gbk')
        for file_name in ftp_list:
            zf.write(file_name)
            os.remove(file_name)

    ftp = FTP()  # 设置变量
    ftp.connect("110.249.163.246", 21)  # 连接的ftp sever和端口
    ftp.login("dc5", "qwer$#@!")  # 连接的用户名，密码如果匿名登录则用空串代替即可
    filepath = datetime.datetime.now().strftime("%Y%m%d")
    # filename = uuid.uuid1()
    filename = zf_name
    log(filename)
    cmd = 'STOR /{}/{}'.format(filepath, filename)

    ftp.storbinary(cmd, open('ftp/{}'.format(filename), 'rb'))
    log('上传成功')