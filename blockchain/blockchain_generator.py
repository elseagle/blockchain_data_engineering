from pprint import pp
from timeit import default_timer as timer

from nonce_generator import generate_nonce, hash_string


def to_string(miner_: int):
    return str(miner_)


def find_hash(
    last_hash: str, length_of_prefix: int = 4, counter_: int = 1, miner: int = 0
):
    """Finds the hash of the generated nonce

    Parameters
        text: the text to be hashed
        length_of_prefix
        counter_: increments per block
        miner: miner_id
    """
    if counter_ <= 1:
        nonce = generate_nonce((100 - len(str(miner))), length_of_prefix)
        sha256 = hash_string(to_string(miner) + nonce)
    else:
        nonce = generate_nonce(
            (100 - len(str(miner)) - len(last_hash)), length_of_prefix
        )
        sha256 = hash_string(last_hash + to_string(miner) + nonce)
    return sha256, nonce, len(nonce), miner, last_hash


def yield_block():
    """Generator for nonce and hash"""
    counter = 1
    last_hash = None
    miner = None
    blocks = []

    while True:
        prefix = "0000"
        if last_hash:
            x = find_hash(
                length_of_prefix=len(prefix),
                counter_=counter,
                miner=miner,
                last_hash=last_hash,
            )
        else:
            x = find_hash(length_of_prefix=len(prefix), counter_=counter, last_hash="")
        if x[0].startswith(prefix):
            counter += 1
            if len(blocks) == 10:
                break

            last_hash = str(x[0])
            miner = x[3]
            blocks.append({"nonce": x[1], "miner": 0})

            yield blocks


def mine_the_next_block(block):
    """Mines the next block in the chain

    Parameters:
        block: the generator object
    """
    return next(block)


def verify_chain(chain_: list, prefix: str = "0000"):
    """Verifies if the chain sequence is accurate

    Parameters:
        chain_: the list of mined blocks
        prefix: the zero prefix
    """

    verified_count = 0
    for i, block in enumerate(chain_):
        nonce = block["nonce"]
        miner = block["miner"]
        if i < 1:
            hash_ = hash_string(to_string(miner) + nonce)
        else:
            hash_ = hash_string(hash_ + to_string(miner) + nonce)
        if hash_.startswith(prefix):
            verified_count += 1
    if verified_count == len(chain_):
        # print("Verification Successful")
        return True
    else:
        print("Verification Failed")
        return False


if __name__ == "__main__":
    chain = yield_block()
    for _ in range(10):
        block_chain = mine_the_next_block(chain)
    block_chain = list(block_chain)
    pp(block_chain)
    verify_chain(block_chain)
