from setting import cursor, urun, db
import datetime

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(dt, type(dt))
cursor.execute('INSERT INTO dt(dt) VALUES("%s")' % (dt))
db.commit()