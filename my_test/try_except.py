try:

    try:
        raise 1 == 2
    except Exception as e:
        print(e)
        # print(str(e))
        print(type(e))
        raise 1 == 2
except Exception as e:
    print(e)