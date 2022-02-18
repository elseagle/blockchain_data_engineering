import base64
import hashlib
import os
import random
import string
import threading
import time
from pprint import pp
from queue import Queue
from timeit import default_timer as timer

print_lock = threading.Lock()


def generateRandomAlphaNumericString(length):
    # Generate alphanumeric string
    letters = string.ascii_letters + string.digits

    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def generate_nonce(length: int, length_of_padding):
    """
    Generates a random string of bytes, base64 encoded
    """
    if length < 1:
        return ""
    string_ = base64.b64encode(os.urandom(length))
    b64len = 5 * length
    if length % 3 == 1:
        b64len += 2
    elif length % 9 == 1:
        b64len += random.randint(1, 7)
    elif length % 5 == 0:
        b64len += random.randint(3, 9)
    elif length % 7 == 2:
        b64len += random.randint(10, 19)
    # TODO: Explain random logic below

    output = string_[0:b64len].decode()
    if length_of_padding <= 4 and length_of_padding > 0:
        output = output.replace(r"+", "").replace("/", "")

    random_position = random.randint(0, (len(output) - length))
    return output[random_position : length + random_position]


def to_string(miner_: int):
    return str(miner_)


def hash_string(string):
    """
    Return a SHA-256 hash of the given string
    """
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def find_hash(last_hash, length_of_padding=4, counter_=1, miner=0):
    if counter_ <= 1:
        nonce = generate_nonce(99, length_of_padding)
        sha256 = hash_string(to_string(miner) + nonce)
    else:
        nonce = generate_nonce(35, length_of_padding)
        sha256 = hash_string(to_string(miner) + nonce + last_hash)
    return sha256, nonce, len(nonce), miner, last_hash


def find_hash(last_hash, length_of_padding=4, counter_=1, miner=0):
    if counter_ <= 1:
        nonce = generate_nonce(99, length_of_padding)
        sha256 = hash_string(to_string(miner) + nonce)
    else:
        nonce = generate_nonce(35, length_of_padding)
        sha256 = hash_string(to_string(miner) + nonce + last_hash)
    return sha256, nonce, len(nonce), miner, last_hash


def main(counter, miner, last_hash=None, padding="0000"):
    if last_hash:
        x = find_hash(
            length_of_padding=len(padding),
            counter_=counter,
            miner=miner,
            last_hash=last_hash,
        )
    else:
        x = find_hash(
            length_of_padding=len(padding), counter_=counter, last_hash="", miner=miner
        )
    return x


def verify_chain(chain_):
    verified_count = 0
    for i, block in enumerate(chain_):
        nonce = block["nonce"]
        miner = block["miner"]
        if i < 1:
            hash_ = hash_string(to_string(miner) + nonce)
        else:
            hash_ = hash_string(to_string(miner) + nonce + hash_)
        if hash_.startswith("0000"):
            verified_count += 1
    if verified_count == len(chain_):
        print("Verification Successful")
        return True
    else:
        print("Verification Failed")
        return False


class MyThread(threading.Thread):
    def __init__(self, queue, queue2, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.queue2 = queue2
        self.daemon = True
        self.counter = args[0]
        self.miner = args[1]
        self.last_hash = args[2]
        self.padding = args[3]
        self.blocks = args[4]

    def run(self):
        name = threading.currentThread().getName()

        print(
            name,
            "Starting Process A",
        )

        while True:

            x = main(
                counter=self.counter,
                miner=name.replace("Thread-", ""),
                last_hash=self.last_hash,
                padding=self.padding,
            )

            if x[0].startswith(self.padding):
                self.counter += 1
                # if len(self.blocks) == 10:
                #     break

                last_hash = str(x[0])
                miner = x[3]
                nonce = x[1]
                if len(self.blocks) == 0:

                    self.blocks.append(
                        {
                            "nonce": nonce,
                            "miner": miner,
                            "last_hash": last_hash,
                            "counter": self.counter,
                        }
                    )

                    print(
                        threading.currentThread().getName(),
                        "Sending message:",
                        self.blocks,
                    )

                    self.queue.queue.clear()
                    self.queue.put(self.blocks)
                else:
                    print(name, "Block has data already")
                break

    def receive_message(self, name_, updated_queue):
        new_blocks = updated_queue.get()
        print(f"Thread-{str(name_+1)}", "Starting Process B")

        if new_blocks:
            while True:
                last_block = new_blocks[-1]
                new_counter = last_block["counter"]
                last_hash = last_block["last_hash"]

                x = main(
                    counter=new_counter,
                    miner=f"{str(name_+1)}",
                    last_hash=last_hash,
                    padding="0000",
                )

                if x[0].startswith(padding):
                    new_counter += 1
                    if len(new_blocks) == 10:
                        pp(new_blocks)
                        verify_chain(new_blocks)
                        print("DONE")
                        return True

                    last_hash = str(x[0])
                    miner = x[3]
                    print()
                    nonce = x[1]
                    updated_queue.put(new_blocks)
                    new_blocks.append(
                        {
                            "nonce": nonce,
                            "miner": miner,
                            "last_hash": last_hash,
                            "counter": new_counter,
                        }
                    )
                    verify_chain(new_blocks)

                    print(len(new_blocks))
                    print(
                        f"Thread-{str(name_+1)}",
                        "Received message: Block {} added".format(len(new_blocks)),
                    )

                    break


if __name__ == "__main__":
    threads = []
    sample_word_list = []
    number_of_threads_expected = 4  # value can be adjusted
    number_of_messages_per_thread = number_of_threads_expected - 1

    start = timer()
    counter = 1
    padding = "0000"
    last_hash = None
    miner = None
    blocks = []
    q = Queue()

    for t in range(number_of_threads_expected):
        q2 = Queue()
        threads.append(MyThread(q, q2, args=(counter, t, last_hash, padding, blocks)))
        threads[t].start()
        time.sleep(0.1)
    new_blocks = []
    while len(new_blocks) < 10:

        for i, t in enumerate(threads):

            new_blocks = q.get()
            q.put(new_blocks)
            final = t.receive_message(i, q)
            if final:
                break

    # close thread
    for t in threads:
        t.join()
