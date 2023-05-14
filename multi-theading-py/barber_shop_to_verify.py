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

class BarberShop:

    def __init__(self):
        self.current_customer = -1
        self.CHAIRS = 3
        self.occ = 0
        self._lock = threading.Lock()
        self.S = threading.Semaphore(0)
        self.lk = threading.Semaphore(1)
        self.dm = threading.Semaphore(0)
        self.dm2 = threading.Semaphore(0)
    
    def customer(self, no):
        self._lock.acquire()
        print(f"Lock acquired by : {no}")
        if self.occ == self.CHAIRS:
            print(f"Chairs not available, return customer: {no}")
            self._lock.release()
            return
        
        self.occ+=1
        self._lock.release()

        print("Waking up barber")
        self.S.release()
        self.lk.acquire()

        print(f"going for haircut for customer : {no}")
        self.current_customer = no

        self.dm.release()
        self.dm2.acquire()
        self.occ-=1

        print(f"bye bye, Customer done with haircut, : {no}")
        self.lk.release()


    def barber(self):
        
        while True:
            self.S.acquire()
            print(f"Barber waking up")
            self.dm.acquire()
            print(f"Barber reciving the customer : {self.current_customer}")
            print(f"Done Cutting hair for customer : {self.current_customer}")
            
            self.dm2.release()

if __name__ == "__main__":
    shop = BarberShop()
    t = threading.Thread(target=shop.barber, daemon=True)
    t.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(shop.customer, list(range(10)))

    time.sleep(5)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(shop.customer, list(range(5)))

