#!/usr/bin/python3
from task2 import *
def task1():
    machines = all_machine()
    x,y=4,4
    link=[2, 1, 0, 4, 3, 5, 7, 6, 8, 9, 24, 11, 20, 13, 14, 15, 16, 17,18, 19, 12, 21, 22, 23, 10, 25]
    en = [enigma(link,machines[l%26][y]) for l in range(x,x-6,-1)]
    # en.append(enigma(link,machines[x-6][y-1]))
    checkit=''
    for j in range(6):
        checkit+=chr(en[j](I[j])+97)
    print(checkit)
if __name__ == "__main__":
    print("加密结果为：")
    task1()

