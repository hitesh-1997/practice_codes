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


class DiningPhilosohers:

    def __init__(self):
        self.forks = [threading.Semaphore(1) for _ in range(5)]

    def life(self, id):
        while True:
            self._eat(id)
            self._think(id)

    def _think(self, id):
        print(f"Philosopher: {id} thinking...... ")
        time.sleep(100*random.random())

    def _eat(self, id):
        print(f"Philosopher : {id} want to start eating ..... ")
        if id%2==0:
            self._pick( id%5 , id)
            time.sleep(random.random())
            self._pick( (id+4)%5 , id)
        else:
            self._pick( (id+4)%5 , id)
            time.sleep(random.random())
            self._pick( id%5 , id)

        time.sleep(5*random.random())
        print(f"Philosopher: {id} eating.....", flush=True)

        self._put(id%5, id)
        time.sleep(random.random())
        self._put( (id+4)%5, id)

    def _pick(self, i, pid):
        self.forks[i].acquire()
        print(f"Philosopher: {pid} picking fork: {i} .... ")
    
    def _put(self, i, pid):
        self.forks[i].release()
        print(f"Philosopher: {pid} Putting down fork : {i}.... ")


if __name__ == "__main__":
    dp = DiningPhilosohers()
    threads = [threading.Thread(target=dp.life, args=(i, ), daemon=True) for i in range(5) ]

    for t in threads:
        t.start()

    time.sleep(500)

