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


class ReaderWriter:

    def __init__(self):
        self.wrt = threading.Lock()
        self.read_count = 0
        self.cv = threading.Lock()

    def write(self):
        while True:
            self.wrt.acquire()
            print(f"Writing  ..... ")
            time.sleep(random.random())
            self.wrt.release()
            time.sleep(random.random())
    
    def reader(self, i):
        self.cv.acquire()
        self.read_count+=1
        if self.read_count==1:
            print(f"Trying to lock.... ")
            self.wrt.acquire()
        self.cv.release()

        print(f"Reading  ..... {i}")
        time.sleep(random.random())

        self.cv.acquire()
        self.read_count-=1
        if self.read_count==0:
            self.wrt.release()
        self.cv.release()

if __name__ == "__main__":
    tw = ReaderWriter()
    w = threading.Thread(target=tw.write, daemon=True)
    w.start()

    for i in range(10):
        t = threading.Thread(target=tw.reader, args=(i, ))
        t.start()
        # time.sleep(5*random.random())

    time.sleep(100)
