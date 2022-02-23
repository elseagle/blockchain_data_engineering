import base64
import hashlib
import os
import random
import string
from timeit import default_timer as timer


def generateRandomAlphaNumericString(length: int):
    """Generate random alphanumeric string of a specified length

    Parameters:
        length (int): expected length of random string
    """
    letters = string.ascii_letters + string.digits

    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def hash_string(string: str):
    """Return a SHA-256 hash of the given string

    Parameters:
        string (str): text to hashed
    """
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def generate_nonce(length: int, length_of_prefix: int):
    """Generates a random string of bytes, base64 encoded

    Parameters:
        length: expected length for nonce
        length_of_prefix: length of the prefix onf the hash

    """
    if length < 1:
        return ""

    # Generate random byte of specfied length and encode with base64
    string_ = base64.b64encode(os.urandom(length))

    # the block logic below is create a random length...
    # ...that will be enough to get really random combination
    randomizer = 5 * length

    # Use the random length to slice the encoded string and decode
    output = string_[0:randomizer].decode()

    output = output.replace(r"+", "").replace("/", "").replace("+", "")

    # use the length of decoded string...
    # ...and expected output to slice out the random strings
    random_position = random.randint(0, (len(output) - length))
    return output[random_position: length + random_position]


def find_hash(text: str, length_of_prefix: int = 4):
    """Finds the hash of the genrated nonce

    Parameters
        text: the text to be hashed
        length_of_prefix
    """
    random_string = generate_nonce((100 - len(text)), length_of_prefix)

    sha256 = hash_string(text + random_string)
    return sha256, random_string, len(random_string)


if __name__ == "__main__":
    word = input("Kindly input word: ")
    start = timer()
    while True:
        # word below can be any string,
        prefix = "0000"
        x = find_hash(word, len(prefix))
        if x[0].startswith(prefix):
            print("Total Time:", (timer() - start))  # in seconds
            print("SHA256:", x[0])
            print()
            print("NONCE:", x[1])
            print()
            start = timer()
            break
