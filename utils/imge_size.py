# -*- coding: utf-8 -*-


def main():
    import os
    from PIL import Image

    path = os.path.join(os.getcwd(), "115339132.jpg")
    img = Image.open(path)

    print(img.format)
    print(img.size)
    size = 90
    img.resize((size, size), Image.ANTIALIAS).save("icom_%d.png" % (size))


if __name__ == '__main__':
    main()
