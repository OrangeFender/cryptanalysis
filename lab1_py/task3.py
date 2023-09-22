#!/usr/bin/python3
from task2 import *
import time

if __name__ == "__main__":
    start=time.time()
    for i in range(1000):
        task1()
    end=time.time()
    runtime = end - start
    print(f"1000次加密花费时间:{runtime:.6f}s")

