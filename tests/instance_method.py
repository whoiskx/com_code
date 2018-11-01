# -*- coding: utf-8 -*-


class Jests(object):
    def __init__(self):
        self.name = 'gua'

    @staticmethod
    def test():
        return "OK"

    @classmethod
    def __getattr__(cls, item):
        print('not attr')
        # print(item)
        cls.item = item
        print(cls.__name__)
        return item

# def foo(a=[]):
#     a.append(1)
#     print(a)
# foo()
# foo()
# foo()

def greeting(msg):
    def hello(name):
        print(msg, name)

    return hello

#
# f = greeting('are you ok')
#
# print(f)
# print(f("123"))


def main():
    t = Jests()
    print(t.test())
    print(Jests.test())
    print(t.testsasadf)

if __name__ == '__main__':
    main()
