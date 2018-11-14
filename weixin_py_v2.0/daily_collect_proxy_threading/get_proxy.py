# -*- coding: utf-8 -*-
import re

import requests


def abuyun_proxy():

    # 要访问的目标页面
    target_url = "http://test.abuyun.com"

    # 代理服务器
    proxy_host = "http-dyn.abuyun.com"
    proxy_port = "9020"

    # 代理隧道验证信息
    proxy_user = "H47MY63960OG8D8D"
    proxy_pass = "DA3B03DDAEE0CDF7"

    proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_user,
        "pass": proxy_pass,
    }

    proxies = {
        "http": proxy_meta,
        "https": proxy_meta,
    }

    # resp = requests.get(target_url, proxies=proxies)
    #
    # print(resp.status_code)
    # # print(resp.text)
    # s = re.search(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', resp.text)
    # print(s.group())
    # proxies = {
    #     "http": "http://{}:9020".format(s.group()),
    #     "https": "http://{}:9020".format(s.group()),
    # }
    # print(proxies)
    return proxies


if __name__ == '__main__':
    html = '''<!DOCTYPE html>
    <head>
    <link rel="stylesheet" href="/misc/styles/proxy.css">
    </head>
    <body>
    <table>

    <tr><th>protocol</th><td>HTTP/1.1</td></tr>
    <tr><th>request-method</th><td>GET</td></tr>
    <tr><th>client-ip</th><td>114.216.121.48</td></tr>
    <tr class="sep"><th>&nbsp;</th><td>&nbsp;</td></tr>
    <tr><th>accept</th><td>*/*</td></tr>
    <tr><th>accept-encoding</th><td>gzip</td></tr>
    <tr><th>connection</th><td>keep-alive</td></tr>
    <tr><th>host</th><td>test.abuyun.com</td></tr>
    <tr><th>user-agent</th><td>python-requests/2.12.4</td></tr>
    </table>
    </body>
    </html>'''
    abuyun_proxy()
