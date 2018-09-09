# -*- coding: utf-8 -*-
import time

from images.tests import O
o = O()
count = 1
while True:
    print(o.name)
    count += 1
    o.name = {'af':count}
    print(o.name)
    time.sleep(1)
