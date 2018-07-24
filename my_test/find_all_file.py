# import os
#
# dir_file = os.path.abspath(__file__)
# dir_folder = os.path.dirname(dir_file)
# dir_x = os.path.basename(dir_file)
#
# print(dir_file, dir_folder, '\n', dir_x)
#
# def foo(folder):
#     while True:
#         if os.path.isdir(folder):
#             return foo()


from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
_input = browser.find_element_by_class_name('anchor')
print(input.text)
print(_input.text)