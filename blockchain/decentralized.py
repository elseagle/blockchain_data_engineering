import threading
import time
from pprint import pp
from queue import Queue
from timeit import default_timer as timer
from blockchain_generator import verify_chain, find_hash


def main(counter: int, miner, last_hash: str = "", padding="0000"):
    """Generates hash based on last hash

    Parameters:
        counter: increments on every block
        miner: current block's miner
        last_hash: hash from last block mine
        padding: the zero padding
    """
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


class MyThread(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
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
            "Starting intial mine...",
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
                    self.queue.put(blocks)

                    print(
                        threading.currentThread().getName(),
                        "Sending message:",
                        self.blocks,
                    )

                else:
                    print(name, "Block has data already")
                break
            if len(self.blocks) != 0:
                self.mine_the_next_block(self.miner, self.queue)

    def mine_the_next_block(self, name_, updated_queue):
        # get block from queue
        new_blocks = updated_queue.get()
        print(f"Thread-{str(name_)}", "Mining next block...")

        if new_blocks:
            while True:
                if len(new_blocks) > 9:
                    break
                last_block = new_blocks[-1]
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
                    new_blocks.append(
                        {
                            "nonce": nonce,
                            "miner": miner,
                            "last_hash": last_hash,
                            "counter": new_counter,
                        }
                    )
                    verify_chain(new_blocks, self.padding)
                    updated_queue.put(new_blocks)

                    print(len(new_blocks))
                    print(
                        f"Thread-{str(name_)}",
                        "Sending message: Block {} added".format(len(new_blocks)),
                    )
                    if len(new_blocks) == 10:
                        for block in new_blocks:
                            del block["counter"]
                            del block["last_hash"]
                        pp(new_blocks)
                        verify_chain(new_blocks, self.padding)
                        print("DONE")
                        updated_queue.queue.clear()
                        updated_queue.task_done()
                        return updated_queue


if __name__ == "__main__":
    threads = []
    sample_word_list = []
    number_of_threads_expected = 6  # value can be adjusted

    start = timer()
    counter = 1
    padding = "0000"
    last_hash = ""
    miner = None
    blocks = []
    q = Queue()

    for t in range(number_of_threads_expected):

        miner = t + 1
        threads.append(MyThread(q, args=(counter, miner, last_hash, padding, blocks)))
        threads[t].start()
        time.sleep(0.1)

    # close thread
    for t in threads:
        t.join()
