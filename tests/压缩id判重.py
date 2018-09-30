# -*- coding: utf-8 -*-
import zlib, urllib
from urllib import request

import requests
# 得到的id列表里面的id再底层检索不到

def main():
    fp = request.urlopen('http://60.191.133.36:8001/loadurls?id=51089477')
    str1 = fp.read()
    fp.close()
    print(str1)
    # ---- 压缩数据流。
    # str3 = zlib.compress(str1, zlib.Z_BEST_COMPRESSION)
    str2 = zlib.decompress(str1, 16+zlib.MAX_WBITS)
    # print(list(str2))
    # print(
    #     len(str3), str3)
    print(
        len(str2), str(str2))


if __name__ == '__main__':
    main()
