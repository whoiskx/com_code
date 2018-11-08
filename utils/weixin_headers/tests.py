# -*- coding: utf-8 -*-


def main():
    import os
    filePath = 'D:\WXSchedule\Images'
    for i, j, k in os.walk(filePath):
        print(i, j, k)
        break

if __name__ == '__main__':
    main()
