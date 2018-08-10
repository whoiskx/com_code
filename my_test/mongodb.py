from setting import urun
import datetime
d = {
    'time': datetime.datetime.now() # .strftime("%Y-%m-%d %H:%M:%S")
}

urun.test.insert(d)