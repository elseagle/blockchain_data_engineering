from concurrent.futures import thread
import random
import string
import threading
import time 
from queue import Queue


print_lock = threading.Lock()


def generateRandomAlphaNumericString(length):
    # Generate alphanumeric string
    global result_str
    letters = string.ascii_letters + string.digits

    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str

class MyThread(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.receive_messages = args[0]
        self.expected_messages = args[1]

    def run(self):
        print (threading.currentThread().getName(), "Sending message:" ,self.receive_messages)
        for _ in range(self.expected_messages):
            val = self.queue.get()
            if val is None:   # If you send `None`, the thread will exit.
                return
            self.do_thing_with_message(val)

    def do_thing_with_message(self, message):
        if self.receive_messages:
            with print_lock:
                print(threading.currentThread().getName(), "Received message:{}".format(message))

if __name__ == '__main__':
    threads = []
    wl = []
    number_of_threads_expected = 3
    number_of_messages_per_thread = number_of_threads_expected - 1
    for t in range(3):
        q = Queue()
        w =generateRandomAlphaNumericString(4)
        
        wl.append(w)
        threads.append(MyThread(q, args=(w,number_of_messages_per_thread)))
        threads[t].start()
        time.sleep(0.1)

    for i, t in enumerate(threads):

        m = wl.copy()
        m.remove(wl[i])
        [t.queue.put(word) for word in m]


    for t in threads:
        t.join()