# Decentralized Blockchain

## About
This section is divided into 5, where each section matches with given descriptions in the given exercise. The following are solution to the exerises according to numbering:
1. Nonce Generator
2. Blockchain Generator
3. Multithreading
4. Thread Communication
5. Decentralized Blockchain


## Nonce Generator (nonce_generator.py)

The goal of this exercise is to generate a nonce.  Given a string, pad it on the right with random alphanumeric characters such that the padded string is 100 in length and its SHA256 hash starts with “0000”. Please search online for how to compute the SHA265 hash in your language. Three main functions are used to achieve this:
1. generate_nonce
   
   This function generates a random set of string/bytes using `os.urandom`, `base64`, and extra random logic that creates more random strings.

2. hash_string
    
    This converts any given string into SHA256

3. find_hash
   
   This hashes the text and the noce combined as one string

Sample input:

'Certik'

Sample Output:
    
    Total Time: 0.45311223599999995
    SHA256: 00003426a1eb9052029ee06dca495208b3682ae51553839bc905ac98d7ea1ebd
    NONCE:FARLF3UsbCDhqipD3dkEIvKSKe1NvnB5BnfvaLfwWQZjI9FtEfSDOyCPq4yCsK396fMcxYz7uFRlyzb8Flufk3pTOiaKnt

Where the total time is in seconds.

**Questions**:
1. On average, how long does it take to find the nonce?\
     Ans: 0.4 secs

2. What if it's require the hash to start with five zeros instead of four?\
    Ans: It takes an average of 5 secs

## Blockchain Generator (blockchain_generator.py)
This uses the 3 main functions from the `Nonce Generator` as a building block. Extra functions created and used here are:
1. yield_block
   This function initiates an iterator(generator) that creates a `block` per call.
2. mine_next_block:
   This function creates each block when called on the output of `yield_block`
3. verify_chain
   This function confirms if the chain has been built successfully by reinitiating the chain hash via nonce and the miner.

Sample Output:
    
    [{'nonce': 'h0XuDhFzwGXdR3HAwk3pFCgFWGnSc1xGfm4n7kLB2uJhnQTatcbNIjjvGedF7YkMTUtxFS2HWyrBKiaPK0DW9qPrOPqeqjgcH7I','miner': 0},
    {'nonce': '131WDzjL2yb517jrjcKbUP7Qw2xQngqSpk=', 'miner': 0},
    {'nonce': 'KgwjcJLmkoGaVDKIytA4FidCACgIyGPx4k=', 'miner': 0},
    {'nonce': '7ilsTaypO51vrAUWXNtjwZlcDBH9QdcKcXS', 'miner': 0},
    {'nonce': 'woEKk1ovKFPJlrDVsXYV0KPwKY5nLZATyLa', 'miner': 0},
    {'nonce': 'AtdtRIAuJUy1UfmOn5ycFkS7W37qUIuGzvr', 'miner': 0},
    {'nonce': 'qq46Mme9uOY1nvnCyJqsBbiKAnKlyipnJra', 'miner': 0},
    {'nonce': 'j97WJ6PYbZYcyDeo7fJtIVdwTdkTevHG0oM', 'miner': 0},
    {'nonce': '5qt2lrEUoxid7ndBHESGh3tPojrVQYon56R', 'miner': 0},
    {'nonce': '17vZ0psHHXskyb61DZrAsEnkB409zCG7UUv', 'miner': 0}]

## Multithreading (multithreading_generator.py)
This script uses three threads and sends unique message per thread. There is just one function (generateRandomAlphaNumericString) that each thread uses to send their unique messages

Sample Output:
    
    Thread:1: BDoNow2NyHAqt6PNjgG
    Thread:2: bz0pBIhbyvBeTAG
    Thread:3: SBkP70TtOJpezIKC2

  
## Thread Communication (thread_communication.py)
