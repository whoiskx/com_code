# from pyquery import PyQuery as pq
#
# html = '<img xmlns="http://www.w3.org/1999/xhtml" class="scaledImageFitHeight img" src="https://scontent-hkg3-1.xx.fbcdn.net/v/t1.0-0/s480x480/37904259_1124867954318375_6151091198841847808_n.jpg?_nc_cat=0&amp;oh=26c5798fac6fcc34a016ec2b4baaec35&amp;oe=5BCC0063" style="left:-20px;" alt="&#x56FE;&#x7247;&#x4E2D;&#x53EF;&#x80FD;&#x6709;&#xFF1A;4 &#x4F4D;&#x7528;&#x6237;&#x3001;&#x5FAE;&#x7B11;&#x7684;&#x7528;&#x6237;&#x3001;&#x4E00;&#x7FA4;&#x4EBA;&#x5750;&#x7740;&#x548C;&#x5B69;&#x5B50;" width="357" height="476"/>'
# e = pq(html)
# print(e('.scaledImageFitHeight').attr('src'))
import time

from selenium import webdriver
dirver = webdriver.Chrome()
url = 'https://www.facebook.com/pages/%E8%B5%A4%E6%9F%B1%E8%AD%A6%E7%BD%B2/144577805604437?rf=238224856304628'
dirver.get(url)
time.sleep(1000)