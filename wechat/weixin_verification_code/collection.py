import requests
# from selenium import webdriver

# driver = webdriver.Chrome()
for i in range(1000):
    print(i)
    url = 'http://mp.weixin.qq.com/mp/verifycode?cert=1543976808853.3088'
    # driver.get(url)
    r = requests.get(url)
    with open('img/{}.png'.format(i), 'wb') as f:
        f.write(r.content)
    # if i > 5:
    #     break