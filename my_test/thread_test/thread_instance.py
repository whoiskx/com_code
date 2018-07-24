import _thread
import time


def print_time(thread_name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print('{} : {}'.format(thread_name, time.ctime(time.time())))


try:
    _thread.start_new_thread(print_time, ('Thread-1', 2))
    _thread.start_new_thread(print_time, ('Thread-2', 4))
except Exception as e:
    print(e)

time.sleep(100)

print('end')