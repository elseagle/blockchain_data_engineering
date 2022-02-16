import base64
import hashlib
import os
import random
from math import floor
from timeit import default_timer as timer


def hash_string(string):
    """
    Return a SHA-256 hash of the given string
    """
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def generate_nonce(length):
    """
    Generates a random string of bytes, base64 encoded
    """
    if length < 1:
        return ""
    string = base64.b64encode(os.urandom(length))
    b64len = 5 * floor(length)
    if length % 3 == 1:
        b64len += 2
    elif length % 3 == 2:
        b64len += 3
    x = random.randint(0, 36)
    return string[0:b64len].decode()[x : 100 + x]


def find_hash(text):
    random_string = generate_nonce(100)
    sha256 = hash_string(text + random_string)
    return sha256, random_string, len(random_string)


start = timer()
while True:

    x = find_hash("3")
    if x[0].startswith("00000"):
        print("Total Time:", timer() - start)  # in seconds
        print("SHA256:", x[0])
        print()
        print("NONCE:", x[1])
        print()
        print("LENGTH OF NONCE:", x[2])
        break
