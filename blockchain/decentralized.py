import base64
from concurrent.futures import thread
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
    def __init__(self, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
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

        while len(self.blocks) < 10:

            x = main(
                counter=self.counter,
                miner=name.replace("Thread-", ""),
                last_hash=self.last_hash,
                padding=self.padding,
            )

            if x[0].startswith(self.padding):
                self.counter += 1
                if len(self.blocks) == 10:
                    return True

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

                else:
                    print(name, "Block has data already")
                break
            if len(self.blocks) != 0:
                f = self.mine_next_block(self.miner)

    def mine_next_block(self, name_):

        print(f"Thread-{str(name_)}", "Starting Process B")

        if self.blocks:
            while len(self.blocks) < 10:
                last_block = self.blocks[-1]
                new_counter = last_block["counter"]
                last_hash = last_block["last_hash"]

                x = main(
                    counter=new_counter,
                    miner=f"{str(name_)}",
                    last_hash=last_hash,
                    padding=self.padding,
                )

                if x[0].startswith(padding):
                    new_counter += 1

                    last_hash = str(x[0])
                    miner = x[3]
                    print()
                    nonce = x[1]
                    self.blocks.append(
                        {
                            "nonce": nonce,
                            "miner": miner,
                            "last_hash": last_hash,
                            "counter": new_counter,
                        }
                    )
                    verify_chain(self.blocks)

                    print(len(self.blocks))
                    print(
                        f"Thread-{str(name_)}",
                        "Sending message: Block {} added".format(len(self.blocks)),
                    )
                    if len(self.blocks) == 10:
                        pp(self.blocks)
                        verify_chain(self.blocks)
                        print("DONE")
                        return True

                    break


if __name__ == "__main__":
    threads = []
    sample_word_list = []
    number_of_threads_expected = 6  # value can be adjusted
    number_of_messages_per_thread = number_of_threads_expected - 1

    start = timer()
    counter = 1
    padding = "0000"
    last_hash = None
    miner = None
    blocks = []

    for t in range(number_of_threads_expected):
        q2 = Queue()
        miner = t + 1
        threads.append(MyThread(args=(counter, miner, last_hash, padding, blocks)))
        threads[t].start()
        time.sleep(0.1)

    # close thread
    for t in threads:
        t.join()
