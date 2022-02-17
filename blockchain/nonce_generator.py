import base64
import hashlib
import os
import random
import string
from timeit import default_timer as timer


def generateRandomAlphaNumericString(length):
    # Generate alphanumeric string
    letters = string.ascii_letters + string.digits

    result_str = ''.join(random.choice(letters) for i in range(length))
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
        b64len +=random.randint(10, 19)
    # TODO: Explain randomlogic below
    output = string_[:b64len].decode()
    if length_of_padding <=4 and length_of_padding >0:
        output = output.replace(r"+", "").replace("//", "")

    
    random_position = random.randint(0, (len(output)-100))
    return output[random_position : 100 + random_position]


def find_hash(text, length_of_padding=4):
    random_string = generate_nonce(100, length_of_padding)
    sha256 = hash_string(text + random_string)
    return sha256, random_string, len(random_string)


start = timer()
count = 0
while True:

    word = generateRandomAlphaNumericString(1) # can be replaced with any word
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
