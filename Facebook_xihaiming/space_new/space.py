import time

from pyquery import PyQuery as pq
import re
from setting import driver_facebook, execute_times, urun, log


class SpaceData(object):
    def __init__(self, time='', original='', comment_sum='', share='', praise='', content=''):
        self.time = time
        self.original = original
        self.comment_sum = comment_sum
        self.share = share
        self.praise = praise
        self.content = content

    def obj_to_dict(self):
        return self.__dict__



try:
    driver = driver_facebook()
    driver.get('https://www.facebook.com/profile.php?id=100018160331338')
    time.sleep(3)
    execute_times(driver, 2000)
    html = driver.page_source
    with open('index_xihaiming.html', 'w', encoding='utf-8') as f:
        f.write(html)
except Exception as e:
    log('safdafas', e)
    html = driver.page_source
    with open('index_xihaiming_error.html', 'w', encoding='utf-8') as f:
        f.write(html)