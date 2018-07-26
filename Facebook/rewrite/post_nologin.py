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
from xml.etree.ElementTree import ElementTree, Element

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
    print(Author, PortraitUrl, ImageUrl, Praises, Comments, Transmits)

    xml_node_dict = {
        "author": Author,
        "portraitUrl": PortraitUrl,
        "imageUrl": ImageUrl,
        "praises": Praises,
        "comments": Comments,
        "transtmis": Transmits,
        "content": Content,
        "headurl": PortraitUrl,
    }
    return xml_node_dict

    # xml_sample = ['site', 'content', 'author', 'time', 'url', 'authorID', 'imageUrl', 'transtmis', 'comments', 'hash',
    #          'blogid', 'uid', 'imgCounts', 'source', 'qimgCounts']
    #
    # doc = Document()
    # root = doc.createElement('Blog')
    # doc.appendChild(root)
    # for node in xml_sample:
    #     node_append = doc.createElement(node)
    #     if node in xml_node_dict.keys():
    #         node_xml = doc.createElement(node)
    #         text = xml_node_dict[node]
    #         node_text = doc.createTextNode(text)
    #         node_xml.appendChild(node_text)
    #         root.appendChild(node_xml)
    #         continue
    #     root.appendChild(node_append)
    #
    # import hashlib
    # import time
    # curent_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
    # xml_name = Author + curent_time
    # m = hashlib.md5()
    # m.update(xml_name.encode('utf-8'))
    # xml_file_name = m.hexdigest()
    # with open('{}.xml'.format(xml_file_name), 'w', encoding='utf-8') as f:
    #     doc.writexml(f, addindent='\t', newl='\n', encoding="utf-8")


def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    '''将xml文件写出
       tree: xml树
       out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


# ---------------search -----
def find_nodes(tree, path):
    '''查找某个路径匹配的所有节点
       tree: xml树
       path: 节点路径'''
    return tree.findall(path)


def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''改变/增加/删除一个节点的文本
       nodelist:节点列表
       text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text


def nodes_add_text(tree, node, content):
    text_nodes = find_nodes(tree, node)
    change_node_text(text_nodes, content)


def write_data_to_xml(data):
    tree = read_xml("model_fb.xml")
    for d in data.keys():
        nodes_add_text(tree, d, data.get(d))
        write_xml(tree, "new_fb.xml")


def main():
    url = 'https://www.facebook.com/permalink.php?story_fbid=2163264660369593&id=188533647842714'
    data = get_post_details(url)
    write_data_to_xml(data)


if __name__ == '__main__':
    main()
