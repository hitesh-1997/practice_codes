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

class UberRide:
    def __init__(self):
        self.cv_demo = threading.Semaphore()
        self.cv_repu = threading.Semaphore()
        self._lock = threading.Lock()
        self._demo_count = 0
        self._repub_count = 0
        self.barr = threading.Barrier(4)

    def bookTaxi(self, type):
        if type=="Demo":
            self._bookDemocrate()
        else:
            self._bookRepublican()
    
    def _bookDemocrate(self):
        is_main_driver = False

        self._lock.acquire()

        self._demo_count+=1
        if self._demo_count==4:
            is_main_driver = True
            self.cv_demo.release(3)
            self._demo_count-=4
        elif self._demo_count==2 and self._repub_count>=2:
            is_main_driver = True
            self.cv_demo.release(1)
            self.cv_repu.release(2)
            self._demo_count-=2
            self._repub_count-=2
        else:
            self._lock.release()
            print(f"Democrates waiting with count: {self._demo_count}")
            self.cv_demo.acquire()
            

        time.sleep(5*random.random())
        self.barr.wait()

        print(f"Democrate seated at the position..... ")

        if is_main_driver:
            print(f"Instructing driver to drive..... ")
            self._lock.release()

    def _bookRepublican(self):
        is_main_driver = False

        self._lock.acquire()
        self._repub_count+=1

        if self._repub_count==4:
            is_main_driver = True
            self.cv_repu.release(3)
            self._repub_count-=4
        elif self._demo_count==2 and self._repub_count>=2:
            is_main_driver = True
            self.cv_demo.release(2)
            self.cv_repu.release(1)
            self._repub_count-=2
            self._demo_count-=2
        else:
            self._lock.release()

            print(f"Republicans waiting with count: {self._repub_count}")
            self.cv_repu.acquire()

        time.sleep(5*random.random())
        self.barr.wait()
        
        print(f"Republican seated at the position..... ")

        if is_main_driver:
            print(f"Instructing driver to drive..... ")
            self._lock.release()


if __name__ == "__main__":
    uber = UberRide()
    # users = [i%2 for i in range(4*5)]
    # random.shuffle(users)

    users = [0, 1, 1, 0, 1, 1, 0, 0]
    

    for i in users:
        user_type = "Demo" if i==0 else "Repub"
        t = threading.Thread(target=uber.bookTaxi, args=(user_type, ))
        t.start()
        time.sleep(random.random())
        

    time.sleep(100)

    




