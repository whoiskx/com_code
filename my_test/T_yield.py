i = 0

def generater():
    global i
    i += 1
    yield i

def foo():
    global i
    i += 1
    return i


# x = generater()
# print(next(x))
# print(next(x))
# print(next(x))

print(foo())