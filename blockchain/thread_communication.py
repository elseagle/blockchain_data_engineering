import random
import string
import threading
import time
from queue import Queue


print_lock = threading.Lock()


def generateRandomAlphaNumericString(length):
    # Generate alphanumeric string
    letters = string.ascii_letters + string.digits

    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


class MyThread(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.received_message = args[0]
        self.expected_messages = args[1]

    def run(self):
        print(
            threading.currentThread().getName(),
            "Sending message:",
            self.received_message,
        )
        for _ in range(self.expected_messages):
            val = self.queue.get()
            if val is None:  # If you send `None`, the thread will exit.
                return
            self.receive_message(val)

    def receive_message(self, message):
        if self.received_message:
            with print_lock:
                print(
                    threading.currentThread().getName(),
                    "Received message:{}".format(message),
                )


if __name__ == "__main__":
    threads = []
    sample_word_list = []
    number_of_threads_expected = 3
    number_of_messages_per_thread = number_of_threads_expected - 1
    for t in range(number_of_threads_expected):
        q = Queue()
        sample_word = generateRandomAlphaNumericString(4)

        sample_word_list.append(sample_word)
        threads.append(MyThread(q, args=(sample_word, number_of_messages_per_thread)))
        threads[t].start()
        time.sleep(0.1)

    for i, t in enumerate(threads):

        word_list_copy = sample_word_list.copy()
        # this removes the current thread's message, it shouldn't recieve its own message again
        word_list_copy.remove(sample_word_list[i])
        [t.queue.put(word) for word in word_list_copy]

    # close thread
    for t in threads:
        t.join()
