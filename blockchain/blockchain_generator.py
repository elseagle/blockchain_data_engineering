import base64
import hashlib
import os
from pprint import pp
import random
from timeit import default_timer as timer
from nonce_generator import hash_string, generate_nonce


def to_string(miner_: int):
    return str(miner_)


def find_hash(
    last_hash: str, length_of_padding: int = 4, counter_: int = 1, miner: int = 0
):
    """Finds the hash of the genrated nonce

    Parameters
        text: the text to be hashed
        length_of_padding
        counter_: increments per block
        miner: miner_id
    """
    if counter_ <= 1:
        nonce = generate_nonce(99, length_of_padding)
        sha256 = hash_string(to_string(miner) + nonce)
    else:
        nonce = generate_nonce(35, length_of_padding)
        sha256 = hash_string(to_string(miner) + nonce + last_hash)
    return sha256, nonce, len(nonce), miner, last_hash


def yield_nonce_and_hash():
    """Generator for nonce and hash"""
    start = timer()
    counter = 1
    last_hash = None
    miner = None
    blocks = []

    while True:
        padding = "0000"
        if last_hash:
            x = find_hash(
                length_of_padding=len(padding),
                counter_=counter,
                miner=miner,
                last_hash=last_hash,
            )
        else:
            x = find_hash(
                length_of_padding=len(padding), counter_=counter, last_hash=""
            )
        if x[0].startswith(padding):
            counter += 1
            if len(blocks) == 10:
                break

            print("Total Time:", (timer() - start))  # in seconds
            print("SHA256:", x[0])
            last_hash = str(x[0])
            miner = x[3]
            print()
            start = timer()
            blocks.append({"nonce": x[1], "miner": 0})

            yield blocks


def mine_the_next_block(block):
    """Mines the next block in the chain
    
    Paramenters:
        block: the generator object 
    """
    return next(block)


def verify_chain(chain_: list, padding: str = "0000"):
    """Verifies if the chain sequence is accurate

    Parameters:
        chain_: the list of mined blocks
        padding: the zero padding
    """

    verified_count = 0
    for i, block in enumerate(chain_):
        nonce = block["nonce"]
        miner = block["miner"]
        if i < 1:
            hash_ = hash_string(to_string(miner) + nonce)
        else:
            hash_ = hash_string(to_string(miner) + nonce + hash_)
        if hash_.startswith(padding):
            verified_count += 1
    if verified_count == len(chain_):
        print("Verification Successful")
        return True
    else:
        print("Verification Failed")
        return False


if __name__ == "__main__":
    chain = yield_nonce_and_hash()
    for _ in range(10):
        block_chain = mine_the_next_block(chain)
    block_chain = list(block_chain)
    pp(block_chain)
    verify_chain(block_chain)
