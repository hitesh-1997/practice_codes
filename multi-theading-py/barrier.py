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

class Barrier:

    def __init__(self, n):
        self.n = n
        self._count = 0
        self.cv = threading.Condition()

    def wait(self, id):
        self.cv.acquire()
        self._count+=1
        if self._count<self.n:
            print(f"Thread: {id} Waiting .... ")
            self.cv.wait()
        elif self._count==self.n:
            self.cv.notify_all()
        
        # release here b/c when wait done, thread re-acquire lock which needs to be released again
        self.cv.release()

class Dummy:

    def critical(self, id, b: Barrier):
        b.wait(id)
        print(f"Executing thread: {id}")

if __name__ == "__main__":
    NUM = 5
    bar = Barrier(NUM)
    dum = Dummy()

    all_threads = []

    for i in range(NUM):
        t = threading.Thread(target=dum.critical, args=(i, bar, ))
        t.start()
        all_threads.append(t)
        time.sleep(5*random.random())
    
    for t in all_threads:
        t.join()

    # time.sleep(100)






