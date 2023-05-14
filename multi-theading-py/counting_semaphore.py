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

class MySemaphore:
    def __init__(self, n):
        self.n = n
        self.count = n
        self.cv = threading.Condition()

    def lock(self):
        self.cv.acquire()
        while self.count==0:
            self.cv.wait()
        self.count-=1
        self.cv.notify()
        self.cv.release()
    
    def unlock(self):
        self.cv.acquire()
        while self.count==self.n:
            self.cv.wait()
        self.count+=1
        self.cv.notify()
        self.cv.release()

class Demo:
    def __init__(self, n):
        self.sema = MySemaphore(n)
        self.lock = threading.Lock()
        self.count = 0

    def critical(self):
        self.sema.lock()
        with self.lock:
            self.count+=1
        
        print(f"Priting critical section with count : {self.count}")
        time.sleep(5*random.random())
        
        with self.lock:
            self.count-=1
        self.sema.unlock()

if __name__ == "__main__":
    dm = Demo(3)
    for _ in range(10):
        t = threading.Thread(target=dm.critical)
        t.start()
    time.sleep(100)