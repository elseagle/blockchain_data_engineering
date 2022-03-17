import random
import threading
import time
from queue import Queue

from nonce_generator import generateRandomAlphaNumericString

print_lock = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.to_be_sent = args[0]
        self.expected_messages = args[1]

    def run(self):

        print(
            threading.currentThread().getName(),
            "Sending message:",
            self.to_be_sent,
        )
        for _ in range(self.expected_messages):
            val = self.queue.get()
            if val is None:  # If you send `None`, the thread will exit.
                return
            self.receive_message(val)

    def receive_message(self, message):
        if self.to_be_sent:
            # The lock makes the thread print it received message before exiting
            with print_lock:
                print(
                    threading.currentThread().getName(),
                    "Received message:{}".format(message),
                )


if __name__ == "__main__":
    threads = []
    sample_word_list = []
    number_of_threads_expected = random.randint(2, 6)  # value can be adjusted

    # the number of messages to be processed by a thread is k-1
    # where k is the number of threads
    number_of_messages_per_thread = number_of_threads_expected - 1
    for t in range(number_of_threads_expected):
        q = Queue()

        # this is the unique message to be sent by thread
        sample_word = generateRandomAlphaNumericString(4)

        sample_word_list.append(sample_word)
        threads.append(MyThread(q, args=(sample_word, number_of_messages_per_thread)))
        threads[t].start()
        time.sleep(0.1)

    for i, t in enumerate(threads):

        word_list_copy = sample_word_list.copy()
        # this removes the current thread's message, it shouldn't recieve its own message again
        word_list_copy.remove(sample_word_list[i])

        #  insert messages into queue
        [t.queue.put(word) for word in word_list_copy]

    # close thread
    for t in threads:
        t.join()
