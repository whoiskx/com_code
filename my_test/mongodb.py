from setting import urun
import datetime
d = {
    'time': datetime.datetime.now() # .strftime("%Y-%m-%d %H:%M:%S")
}
print(d)
urun.test.insert(d)
print(d)