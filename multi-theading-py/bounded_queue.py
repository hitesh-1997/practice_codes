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

class ProducerConsumer:

    def __init__(self, max_size):
        self.q = []
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(max_size)
        self._lock = threading.Lock()
        
    def produce(self):
        self.empty.acquire()
        self._lock.acquire()
        
        time.sleep(10*random.random())
        num = random.random()
        
        self.q.append(num)
        print(f"[Producer] num: {num} into q with sz: {len(self.q)}")

        self._lock.release()
        self.full.release()
    
    def consume(self):
        self.full.acquire()
        self._lock.acquire()
        
        time.sleep(0.2*random.random())
        self.q.pop()
        print(f"[Consumer] num: {self.q[-1]} into q with sz: {len(self.q)}")

        self._lock.release()
        self.empty.release()


if __name__ == "__main__":
    pc = ProducerConsumer(3)

    PRODUCERS = 10
    CONSUMERS = 10

    threads = []
    
    for _ in range(PRODUCERS):
        t = threading.Thread(target=pc.produce)
        t.start()
        threads.append(t)

    for _ in range(CONSUMERS):
        t = threading.Thread(target=pc.consume)
        t.start()
        threads.append(t)

    time.sleep(20)
    for t in threads:
        t.join()
