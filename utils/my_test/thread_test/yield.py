
l = [1,2,3,4,5]
x = range(5)
print(x, type(x))



def te():
    for i in range(5):
        yield i


x  = te()
for i in x:
    print(i)
