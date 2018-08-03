from xml.dom.minidom import Document


# 在内存中创建一个空的文档
doc = Document()


def product_node(node_list=[], target=''):
    for node in node_list:
        node_xml = doc.createElement(node)
        target.appendChild(node_xml)


def xml_create():
    # 创建一个根节点Managers对象
    root = doc.createElement('Blog')
    # 设置根节点的属性
    doc.appendChild(root)

    node_list = ['site', 'content', 'author', 'time', 'url', 'authorID', 'imageUrl', 'transtmis', 'comments', 'hash',
                 'blogid', 'uid', 'imgCounts', 'source', 'qimgCounts']

    product_node(node_list, root)

    user = doc.createElement('User')
    root.appendChild(user)

    node_user_list = ['fans', 'favourites', 'follows', 'headurl', 'name', 'posts', 'sex', 'site', 'uid', 'verified_type']
    product_node(node_user_list, user)

    node_list_2 = ['phrase', 'attitudes_count', 'favorite_count', 'favorite_count', 'atSomeone', 'isComments']
    product_node(node_list_2, root)
    # item = doc.createElement('item')
    # # item.setAttribute('genre','XML')
    # item_text = doc.createTextNode('afasff')
    # item.appendChild(item_text)
    # root.appendChild(item)
    #
    # site = doc.createElement('site')
    # # item.setAttribute('genre','XML')
    # root.appendChild(site)
    #
    # content = doc.createElement('content')
    # # item.setAttribute('genre','XML')
    # root.appendChild(content)
    #
    # author = doc.createElement('author')
    # # item.setAttribute('genre','XML')
    # root.appendChild(author)


    # 将根节点添加到文档对象中
    # doc.appendChild(root)

    # 开始写xml文档
    fp = open('FB_xml.xml', 'w', encoding='utf-8')
    doc.writexml(fp, addindent='\t', newl='\n', encoding="utf-8")


if __name__ == '__main__':
    xml_create()
