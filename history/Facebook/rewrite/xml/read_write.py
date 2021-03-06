from xml.etree.ElementTree import ElementTree, Element


def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    """将xml文件写出
       tree: xml树
       out_path: 写出路径"""
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


if __name__ == "__main__":
    # 1. 读取xml文件
    tree = read_xml("model_fb.xml")

    # 5. 修改节点文本
    # 定位节点
    # text_nodes = find_nodes(tree, "content")
    # change_node_text(text_nodes, "new text")
    nodes_add_text(tree, 'User', "afsdfsafsdaf")

    # 6. 输出到结果文件
    write_xml(tree, "new_fb.xml")
