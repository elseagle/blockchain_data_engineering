import base64
import hashlib
import os
from pprint import pp
import random
import string
from timeit import default_timer as timer


def generateRandomAlphaNumericString(length):
    # Generate alphanumeric string
    letters = string.ascii_letters + string.digits

    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def hash_string(string):
    """
    Return a SHA-256 hash of the given string
    """
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


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
        output = output.replace(r"+", "").replace("//", "")

    random_position = random.randint(0, (len(output) - length))
    return output[random_position : length + random_position]


def to_string(miner_: int):
    return str(miner_)


def find_hash(last_hash, length_of_padding=4, counter_=1, miner=0):
    if counter_ <= 1:
        nonce = generate_nonce(99, length_of_padding)
        sha256 = hash_string(to_string(miner) + nonce)
    else:
        nonce = generate_nonce(35, length_of_padding)
        sha256 = hash_string(to_string(miner) + nonce + last_hash)
    return sha256, nonce, len(nonce), miner, last_hash


def yield_nonce_and_hash():
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
    return next(block)


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


if __name__ == "__main__":
    chain = yield_nonce_and_hash()
    for _ in range(10):
        block_chain = mine_the_next_block(chain)
    block_chain = list(block_chain)
    pp(block_chain)
    verify_chain(block_chain)
