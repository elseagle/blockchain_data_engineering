# Decentralized Blockchain

## About
This section is divided into 5, where each section matches with given descriptions in the given exercise. The following are solution to the exerises according to their numbering:
- [Decentralized Blockchain](#decentralized-blockchain)
  - [About](#about)
  - [Nonce Generator (nonce_generator.py)](#nonce-generator-nonce_generatorpy)
  - [Blockchain Generator (blockchain_generator.py)](#blockchain-generator-blockchain_generatorpy)
  - [Multithreading (multithreading_generator.py)](#multithreading-multithreading_generatorpy)
  - [Thread Communication (thread_communication.py)](#thread-communication-thread_communicationpy)
  - [Decentralized (decentralized.py)](#decentralized-decentralizedpy)


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
In this script, multiple threads are able to communicate with each other i.e send and recieve messages. MyThread is the class used which makes use of the the threading inbuilt class. The major means of communication in this script is done using Queues. Mythread class has two main functions:
  
1. run
   
   This is the initial function that kicks off once the thread is initiated. It is the sender function. It sends the message.

2. receive_message
   
   This function via the queue allows each thread receive a message and log it to the console. A lock is used to ensure the thread prints its received message before exiting.

Sample Output:

    Thread-1 Sending message: sqkg
    Thread-2 Sending message: h7p2
    Thread-3 Sending message: YnTq
    Thread-4 Sending message: 7Bxr
    Thread-5 Sending message: z6lV
    Thread-1 Received message:h7p2
    Thread-2 Received message:sqkg
    Thread-2 Received message:YnTq
    Thread-2 Received message:7Bxr
    Thread-4 Received message:sqkg
    Thread-4 Received message:h7p2
    Thread-4 Received message:YnTq
    Thread-4 Received message:z6lV
    Thread-5 Received message:sqkg
    Thread-3 Received message:sqkg
    Thread-3 Received message:h7p2
    Thread-1 Received message:YnTq
    Thread-1 Received message:7Bxr
    Thread-1 Received message:z6lV
    Thread-2 Received message:z6lV
    Thread-3 Received message:7Bxr
    Thread-5 Received message:h7p2
    Thread-5 Received message:YnTq
    Thread-5 Received message:7Bxr
    Thread-3 Received message:z6lV

## Decentralized (decentralized.py)

This script uses almost same structure to the thread communication script, in terms of MyThread class and communication via queues. There are five main methods in this script:

1. mine_block
   
   This method creates the nth-block by a thread in the chain. Once the block is created, it is broadcasted to all other threads via their individual queues.

2. listen_to_updates
   
   This method listens to the queue to check if there is a new block, if a new block exists, the thread updates its own chain else it continues to mine.

3. validate_and_save_new_chain
   
   This method verifies the current chain passed in and saves the chain if the verification is successful.

4. run
   
   This function has the main logic to continuously mine and listen until the expected number of blocks (10) have been mined in the chain

5. main
   
   This function run the main logic of finding the hash when a new block is to be mined.

Sample Output:

    [{'nonce': '2sp9P0bTbrxlhk867lha3EI3xV6lIkFFxtoWk7O6kjuyfZGiMOiZtUDcoxC39Ut9K400JRIGPWQQDJPmCfozKFa1NNam2aTAmpN','miner': '1'},
    {'nonce': 'eOGwCLTxrcwwB6VXRYCTi0fBpy8Lmw90fK0', 'miner': '2'},
    {'nonce': 'wmKNt1lbXLiSmLxDHXzlQvuxIvXoP5FvBUP', 'miner': '2'},
    {'nonce': 'FSfLwVtMW9ZjwYMI1fQHP1Ht81JTXUivAMK', 'miner': '5'},
    {'nonce': '7U4ipXSaHlUiFtMmgiOBQ3NLcROdLxu0cQ=', 'miner': '3'},
    {'nonce': 'eBnxxUaqeqDED0VY9a9xD54EOycKdrJKRf4', 'miner': '6'},
    {'nonce': 'Xf6n34CME7B2kEdz0sNNIWdC7HmdpcKywkM', 'miner': '3'},
    {'nonce': 'vriu06pJWLOj8j4XsU0PNH1iMkl2bpsbTk=', 'miner': '6'},
    {'nonce': 'HguXWo4lB26yADEh0pStYrNT1CMDOtIJBdt', 'miner': '1'},
    {'nonce': 'VYmEmKSV0DhMSFZgXavY9qRgswLmJRkU5tN', 'miner': '2'}]


More Questions:
1. Does this blockchain scale? What happens when the number of threads go up?

Ans: No, it does not scale, the more the threads the more the queues needed.

2. If one thread stopped working, does it affect the blockchain? What if the thread comes back on later?

Ans: No, it doesn’t affect the chain. If it comes back later, it will pick up the latest chain via the listen_to_updates function.

3. What if we require the SHA256 hashes to start with more zeros?

Ans: It would take a longer time 

4. Is it easy for a “malicious thread” to modify the miner fields in the chain?

Ans: No, because the nonce is gotten from the combination of the last hash[ which container previous miner records].


