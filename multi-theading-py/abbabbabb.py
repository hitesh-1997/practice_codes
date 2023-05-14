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

class Pattern:

    def __init__(self):
        self.S1 = threading.Semaphore(2)
        self.S2 = threading.Semaphore(0)
    
    def A(self):
        while True:
            self.S1.acquire()
            self.S1.acquire()
            
            print("A", end=" ", flush=True)
            time.sleep(random.random())
            
            self.S2.release()
            self.S2.release()
            
    def B(self):
        while True:
            self.S2.acquire()

            print("B", end=" ", flush=True)
            time.sleep(random.random())

            self.S1.release()

if __name__ == "__main__":
    pt = Pattern()
    a = threading.Thread(target=pt.A, daemon=True)
    a.start()
    b = threading.Thread(target=pt.B, daemon=True)
    b.start()
    
    time.sleep(15)