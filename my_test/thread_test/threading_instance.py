import threading
import time

exit_flag = 0


class MyThreading(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print("start {}".format(self.name))
        print_time(self.name, self.counter, 5)
        print("exit {}".format(self.name))


def print_time(thread_name, delay, counter):
    while counter:
        if exit_flag:
            (threading.Thread).exit()
        time.sleep(delay)
        print('{} {}'.format(thread_name, time.ctime(time.time())))
        counter -= 1


thread_1 = MyThreading(1, 'Thread-1', 1)
thread_2 = MyThreading(2, "Thread-2", 2)

thread_1.start()
thread_2.start()

print("exit main thread")
