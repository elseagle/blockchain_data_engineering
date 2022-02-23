import random
import threading
import time
from pprint import pp
from queue import Queue
from timeit import default_timer as timer
from blockchain_generator import verify_chain, find_hash





class MyThread(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.counter = 1
        self.miner = args[1]
        self.last_hash = ""
        self.prefix = "0000"
        self.blocks = []

    @staticmethod
    def main(counter: int, miner, last_hash: str = "", prefix="0000"):
        """Generates hash based on last hash

        Parameters:
            counter: increments on every block
            miner: current block's miner
            last_hash: hash from last block mine
            prefix: the zero prefix
        """
        if last_hash:
            x = find_hash(
                length_of_prefix=len(prefix),
                counter_=counter,
                miner=miner,
                last_hash=last_hash,
            )
        else:
            x = find_hash(
                length_of_prefix=len(prefix), counter_=counter, last_hash="", miner=miner
            )
        return x
    
    def validate_and_save_new_chain(self, latest_block):
        temp_blockchain = self.blocks.copy()
        temp_blockchain.append(latest_block)
        is_valid = verify_chain(temp_blockchain)
        if is_valid:
            self.blocks.append(latest_block)
            self.last_hash = latest_block["last_hash"]
        del temp_blockchain
        return is_valid
    

    def mine_block(self, name):
        if len(self.blocks) > (self.counter - 1):
            self.counter += 1
            return
        x = self.main(
            counter=self.counter,
            miner=f"{str(name)}",
            last_hash=self.last_hash,
            prefix=self.prefix,
        )
        if x[0].startswith(prefix):
            self.counter += 1

            last_hash = str(x[0])
            miner = x[3]
            nonce = x[1]
            new_block = {
                "nonce": nonce,
                "miner": miner,
                "last_hash": last_hash,
                "counter": self.counter,
            }
            self.validate_and_save_new_chain(new_block)

            global queue_list
            # event.clear()
            for q in queue_list:
                q.put(self.blocks)

            if len(self.blocks) == 10:
                for block in self.blocks:
                    del block["counter"]
                    del block["last_hash"]
                pp(self.blocks)
                verify_chain(self.blocks, self.prefix)
                print("DONE")
                self.queue.queue.clear()
                self.queue.task_done()

    def listen_to_updates(self):
        if not self.queue.empty():
            tracking_chain = self.queue.get()
            if len(tracking_chain) > len(self.blocks):
                is_valid = verify_chain(tracking_chain)
                if is_valid:
                    self.blocks = tracking_chain.copy()
                    try:
                        self.last_hash = tracking_chain[-1]["last_hash"]
                    except KeyError:
                        pass


    def run(self):
        name = threading.currentThread().getName()

        print(
            name,
            "Starting initial mine...",
        )
        # event.set()
        while len(self.blocks) < 10:
            self.mine_block(name=self.miner)

            self.listen_to_updates()

   
if __name__ == "__main__":
    threads = []
    sample_word_list = []
    number_of_threads_expected = random.randint(2, 10)  # value can be adjusted

    counter = 1
    prefix = "0000"
    last_hash = ""
    miner = None
    blocks = []
    queue_list = []

    for t in range(number_of_threads_expected):
        q = Queue()
        queue_list.append(q)
        miner = t + 1
        threads.append(
            MyThread(q, args=(counter, miner, last_hash, prefix)))
        threads[t].start()
        time.sleep(0.1)

    # close thread
    for t in threads:
        t.join()
