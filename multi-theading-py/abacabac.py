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

class ABAC:

    def __init__(self):
        self.a = threading.Semaphore(1)
        self.b = threading.Semaphore(0)
        self.c = threading.Semaphore(0)

    def A(self):
        while True:
            self.a.acquire()
            print(f"A", end=" ", flush=True)
            time.sleep(1)

            self.b.release()
            self.c.release()
    
    def B(self):
        while True:
            self.b.acquire()
            print(f"B", end=" ", flush=True)
            time.sleep(1)

            self.a.release()
            self.b.acquire()
    
    def C(self):
        while True:
            self.c.acquire()
            self.c.acquire()
            print(f"C", end=" ", flush=True)
            time.sleep(1)
            
            self.a.release()
    
if __name__ == "__main__":
    pattern = ABAC()
    c = threading.Thread(target=pattern.C)
    c.start()
    time.sleep(1)

    b = threading.Thread(target=pattern.B)
    b.start()
    time.sleep(2)

    a = threading.Thread(target=pattern.A)
    a.start()
    
    time.sleep(100)

    
   
    
    
    






