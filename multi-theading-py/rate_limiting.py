import time
import queue
import threading
import random
import concurrent.futures
import enum
from sys import getrefcount
import functools
import asyncio
from threading import Thread
from threading import Condition
from threading import current_thread
import heapq

import statistics


class RateLimiting:

    def __init__(self):
        self.max_tokens = 20
        self.cv = threading.Condition()
        self.last_time = time.time()
        self.last_tokens = 0

    def get_token(self, i):
        print(f"Requesting token for thread : {i} ...... ")
        self.cv.acquire()
        while time.time()-self.last_time+self.last_tokens < 1:
            self.cv.wait(timeout=1)
        
        new_tokens = min(self.max_tokens, time.time()-self.last_time+self.last_tokens)
        print(f"New tokens : {new_tokens}, Consuming : {i} ... ", flush=True)
        self.last_time = time.time()
        self.last_tokens = new_tokens-1
        self.cv.release()

if __name__ == "__main__":
    rl = RateLimiting()
    time.sleep(5)

    threads = []
    for i in range(10):
        t = threading.Thread(target=rl.get_token, args=(i, ))
        t.start()
    for t in threads:
        t.join()
    