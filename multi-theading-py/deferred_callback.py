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


class DeferredCallback:

    def __init__(self):
        self.pq = []
        self.cv = threading.Condition()

    def add_callback(self, id, timeout):
        self.cv.acquire()
        time_now = time.time()
        execution_timeout = time_now+timeout
        print(f"Adding to queue : {id}, with timeout: {timeout}", flush=True)
        heapq.heappush(self.pq, (execution_timeout, id) )
        self.cv.notify()
        self.cv.release()
    
    def execute_callback(self):
        while True:
            self.cv.acquire()

            while len(self.pq)==0:
                self.cv.wait()
            
            while len(self.pq)>0:
                timeout = self.pq[0][0]-time.time()
                if timeout <= 0:
                    break
                print(f"Waiting for timeout : {timeout} remaining: {len(self.pq)}", flush=True)
                self.cv.wait(timeout=timeout)

            task_name = heapq.heappop(self.pq)
            print(f"Executing task: {task_name[1]}, time diff: {round(time.time()-task_name[0], 2)}", flush=True)
            self.cv.notify()
            self.cv.release()

if __name__ == "__main__":
    dc = DeferredCallback()
    dmn = threading.Thread(target=dc.execute_callback, daemon=True)
    dmn.start()
    time.sleep(1)

    nums = [(1, 10), (2, 5), (3, 6), (4, 11), (5, 2), (6, 6)]
    for id, timeout in nums:
        t = threading.Thread(target=dc.add_callback, args=(id, timeout))
        t.start()
        time.sleep(10*random.random())
    
    threading.Thread(target=dc.add_callback, args=(1, 10)).start()
    time.sleep(3)
    threading.Thread(target=dc.add_callback, args=(2, 5)).start()
    time.sleep(2)
    threading.Thread(target=dc.add_callback, args=(3, 1)).start()
    
    time.sleep(100)

    for t in threads:
        t.join()

    for t in threads:
        print(t.is_alive())