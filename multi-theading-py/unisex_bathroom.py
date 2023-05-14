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

# Extention: Ensure no startvation for one possible gender

class UnisexBathroom:

    def __init__(self):
        self._lock = threading.Condition()
        # -1: None, 0: Male, 1: Female
        self.type = -1
        self._count_lock = threading.Condition()
        self._people = 0
        self._max_people_allowed = 3

    def useBathroom(self, gender_type, id):
        print(f"Enter, gender: {gender_type}, id: {id}")
        # gender_type: [Male, Female]
        gender_int = 0 if gender_type=="Male" else 1

        self._lock.acquire()
        while self.type==1-gender_int:
            self._lock.wait()
        self.type=gender_int
        self._lock.release()

        print(f"Entered after passing Lock condition : {gender_type}, id: {id}")

        self._count_lock.acquire()
        if self._people==self._max_people_allowed:
            print(f"Maximum people exceeded for : {gender_type}, , id: {id}, Waiting in queue.....")
            self._count_lock.wait()
        self._people+=1
        self._count_lock.release()

        print(f"Gender: {gender_type} using Washroom, current number occipued: {self._people}, , id: {id}")
        time.sleep(5*random.random())

        self._count_lock.acquire()
        self._people-=1
        if self._people==0:
            print(f"Done for all : {gender_type}, , id: {id}")
            self._lock.acquire()
            self.type=-1
            self._lock.notify_all()
            self._lock.release()

        # When i released first and than notified, it resulted in error
        print(f"Exiting: {gender_type} with current count: {self._people}")
        self._count_lock.notify()
        self._count_lock.release()
        

if __name__ == "__main__":
    bath = UnisexBathroom()

    male_id = 1
    female_id = 1
    for i in range(20):
        gender_type = "Male" if random.randint(0, 100000)%2==0 else "Female"
        gend_id = male_id if gender_type=="Male" else female_id
        if gender_type=="Male":
            male_id+=1
        else:
            female_id+=1
        
        t = threading.Thread(target=bath.useBathroom, args=(gender_type, gend_id, ) )
        t.start()

        if i>7:
            time.sleep(random.random())
        
    
    time.sleep(100)

