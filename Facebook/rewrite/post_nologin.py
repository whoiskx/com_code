# import requests
#
# url = "https://www.facebook.com/permalink.php?story_fbid=2163264660369593&id=188533647842714"
# proxies = {"https": "https://www.localhost:8000"}
# proxies = {"https": "http://localhost:1080", }
# url =  'https://www.baidu.com/'
# resp = requests.get(url, proxies=proxies)
# print(resp.text)


from utils import driver_facebook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xml.dom.minidom import Document

driver = driver_facebook()


def get_post_details(url):
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fwn")))
    Author = driver.find_element_by_class_name('fwb').text
    # 小头像
    PortraitUrl = driver.find_element_by_class_name('_s0').get_attribute('src')
    # 包含头像
    ImageUrl = driver.find_elements_by_class_name('scaledImageFitWidth')[1].get_attribute('outerHTML')
    # 点赞list
    praise_comment_share = driver.find_elements_by_class_name('_2u_j')
    Praises, Comments, Transmits = '', '', ''
    for item in praise_comment_share:
        if '赞' in item.text:
            Praises = item.text
        if '评论' in item.text:
            Comments = item.text
        if '分享' in item.text:
            Transmits = item.text
    Content = driver.find_element_by_class_name('_5pbx').text
    # print(Author, PortraitUrl, ImageUrl, Praises, Comments, Transmits, Content)


    xml_node_dict = {
            "author": Author,
            "portraitUrl": PortraitUrl,
            "imageUrl": ImageUrl,
            "praises": Praises,
            "comments": Comments,
            "transmits": Transmits,
            "content": Content,
    }
    xml_sample = ['site', 'content', 'author', 'time', 'url', 'authorID', 'imageUrl', 'transtmis', 'comments', 'hash',
             'blogid', 'uid', 'imgCounts', 'source', 'qimgCounts']

    doc = Document()
    root = doc.createElement('Blog')
    doc.appendChild(root)
    for node in xml_sample:
        node_append = doc.createElement(node)
        if node in xml_node_dict.keys():
            node_xml = doc.createElement(node)
            text = xml_node_dict[node]
            node_text = doc.createTextNode(text)
            node_xml.appendChild(node_text)
            root.appendChild(node_xml)
            continue
        root.appendChild(node_append)

    import hashlib
    import time
    curent_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
    xml_name = Author + curent_time
    m = hashlib.md5()
    m.update(xml_name.encode('utf-8'))
    xml_file_name = m.hexdigest()
    with open('{}.xml'.format(xml_file_name), 'w', encoding='utf-8') as f:
        doc.writexml(f, addindent='\t', newl='\n', encoding="utf-8")


if __name__ == '__main__':
    url = 'https://www.facebook.com/permalink.php?story_fbid=2163264660369593&id=188533647842714'
    get_post_details(url)