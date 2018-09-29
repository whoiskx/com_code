# import re
# line = "Cats are smarter than dogs"
# matchObj = re.match(r'(.*) are (.*?) (.*d)', line)
# if matchObj:
#     print("matchObj.group() : ", matchObj.group())
#     print("matchObj.group(0) : ", matchObj.group(0))
#     print("matchObj.group(2) : ", matchObj.group(2))
#     print("matchObj.group(3) : ", matchObj.group(3))
# else:
#     print("No match!!")


import re

content = '333STR1666STR299'
regex = r'([A-Z]+(\d))'

if __name__ == '__main__':
    print(re.match(regex, content)) ##content的开头不符合正则，所以结果为None。

    ##只会找一个匹配，match[0]是regex所代表的整个字符串，match[1]是第一个()中的内容，match[2]是第二对()中的内容。
    match = re.search(regex, content)
    print('\nre.search() return value: ' + str(type(match)))
    print(match.group(0), '==', match.group(1), '==', match.group(2))

    result1 = re.findall(regex, content)
    print('\nre.findall() return value: ' + str(type(result1)))
    for m in result1:
        print(m[0], m[1])

    result2 = re.finditer(regex, content)
    print('\nre.finditer() return value: ' + str(type(result2)))
    for m in result2:
        print(m.group(0), m.group(1), m.group(2))  ##字符串