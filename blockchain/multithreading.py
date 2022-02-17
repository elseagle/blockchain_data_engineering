import random
import string
import threading

result_str = ""


def generateRandomAlphaNumericString(length):
    # Generate alphanumeric string
    global result_str
    letters = string.ascii_letters + string.digits

    result_str = "".join(random.choice(letters) for i in range(length))
    print(f"Thread:{str(threading.current_thread().name)}: {result_str}")
    return result_str


if __name__ == "__main__":
    # creating thread
    # TODO:Make calling K number threads flexible
    t1 = threading.Thread(target=generateRandomAlphaNumericString, args=(19,), name=1)
    t2 = threading.Thread(target=generateRandomAlphaNumericString, args=(15,), name=2)
    t3 = threading.Thread(target=generateRandomAlphaNumericString, args=(17,), name=3)

    # starting threads
    t1.start()
    t2.start()
    t3.start()

    # Stopping Threads
    t1.join()
    t2.join()
    t3.join()

    # All threads completely executed
    print("Done!")
