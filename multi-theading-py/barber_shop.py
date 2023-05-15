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


class BarberShop:

    def __init__(self):
        self._max_customer_allowed = 3
        self._customer_count = 0
        self._count_lock = threading.Lock()
        self._chair  = threading.Semaphore(1)
        self._barber = threading.Semaphore(0)
        self._current_customer_seated = -1
        
    def get_haircur(self, id):
        self._count_lock.acquire()
        if self._customer_count==self._max_customer_allowed:
            print(f"Not enough chairs, leaving customer: {id}", flush=True)
            self._count_lock.release()
            return
        self._customer_count+=1
        self._count_lock.release()

        print(f"Customer: {id} seated at the waiting area", flush=True)

        self._chair.acquire()

        self._current_customer_seated = id

        self._count_lock.acquire()
        self._customer_count-=1
        self._count_lock.release()

        print(f"Customer: {id} seated at the barber chair")
        self._barber.release()
        
    def cut_hair_barber(self):
        while True:
            print(f"Barber sleeping.....")
            self._barber.acquire()
            print(f"Cutting Hair for customer: {self._current_customer_seated}")
            time.sleep(5*random.random())
            self._chair.release()
        

if __name__ == "__main__":
    shop = BarberShop()
    barber_thread = threading.Thread(target=shop.cut_hair_barber, daemon=True)
    barber_thread.start()
    time.sleep(1)

    for i in range(10):
        t = threading.Thread(target=shop.get_haircur, args=(i,))
        t.start()
        time.sleep(random.random())

    time.sleep(100)






        

