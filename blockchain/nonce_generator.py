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


def generate_nonce(length: int, length_of_padding: int):
    """Generates a random string of bytes, base64 encoded

    Parameters:
        length: expected length for nonce
        length_of_padding: length of the padding onf the hash

    """
    if length < 1:
        return ""

    # Generate random byte of specfied length and encode with base64
    string_ = base64.b64encode(os.urandom(length))

    # the block logic below is create a random length...
    # ...that will be enough to get really random combination
    randomizer = 5 * length
    if length % 3 == 1:
        randomizer += 2
    elif length % 9 == 1:
        randomizer += random.randint(1, 7)
    elif length % 5 == 0:
        randomizer += random.randint(3, 9)
    elif length % 7 == 2:
        randomizer += random.randint(10, 19)

    # Use the random length to slice the encoded string and decode
    output = string_[0:randomizer].decode()

    output = output.replace(r"+", "").replace("/", "").replace("+", "")

    # use the length of decoded string...
    # ...and expected output to slice out the random strings
    random_position = random.randint(0, (len(output) - length))
    return output[random_position: length + random_position]


def find_hash(text: str, length_of_padding: int = 4):
    """Finds the hash of the genrated nonce

    Parameters
        text: the text to be hashed
        length_of_padding
    """
    random_string = generate_nonce(100, length_of_padding)

    sha256 = hash_string(text + random_string)
    return sha256, random_string, len(random_string)


if __name__ == "__main__":
    start = timer()

    while True:
        # word below can be any string,
        word = generateRandomAlphaNumericString(1)
        padding = "0000"
        x = find_hash(word, len(padding))
        if x[0].startswith(padding):
            print("Total Time:", (timer() - start))  # in seconds
            print("SHA256:", x[0])
            print()
            print("NONCE:", x[1])
            print()
            print("LENGTH OF NONCE:", x[2])
            print()
            start = timer()
            break
