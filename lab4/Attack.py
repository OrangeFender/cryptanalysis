def left_rotate(number, shift, bits =  32):
    return ((number << shift) | (number >> (bits - shift))) & ((1 << bits) - 1)

def right_rotate(number, shift, bits = 32):
    return ((number >> shift) | (number << (bits - shift))) & ((1 << bits) - 1)

def gen_key(K, r):
    mask = (1 << 64) - 1
    k0 = K >> 64 & mask
    k1 = K & mask
    key = []
    for i in range(r):
        key.append(k0)
        kt = k1
        k1 = k0 ^ left_rotate(k1, 3, 64) ^ left_rotate(k1, 5, 64) ^ i
        k0 = kt

    return key



def ballet_en(plaintext, key, round_):
    n = 1 << 32
    mask = n - 1
    x = []
    ne = [0] * 4
    for i in range(3, -1, -1):
        x.append(plaintext >> (32 * i) & mask)
    # r - 1 轮加密
    for i in range(round_ - 1):
        skl = key[i] >> 32 & mask
        skr = key[i] & mask
        ne[0] = x[1] ^ skl
        ne[1] = ((left_rotate(x[0], 6)) + (left_rotate(x[1] ^ x[2], 9))) % n
        ne[2] = ((left_rotate(x[3], 15)) + (left_rotate(x[1] ^ x[2], 14))) % n
        ne[3] = x[2] ^ skr
        for i in range(4):
            x[i] = ne[i]
    # 第r轮加密
    skl = key[round_ - 1] >> 32 & mask
    skr = key[round_ - 1] & mask
    ne[0] = ((left_rotate(x[0], 6)) + (left_rotate(x[1] ^ x[2], 9))) % n
    ne[1] = x[1] ^ skl
    ne[2] = x[2] ^ skr
    ne[3] = ((left_rotate(x[3], 15)) + (left_rotate(x[1] ^ x[2], 14))) % n

    ciphertext = 0
    for i in range(4):
        ciphertext <<= 32
        ciphertext += ne[i]

    return ciphertext


def attack_low_bit(ctpairs,delta,bits=14):
    mask=(1<<bits)-1
    counter=[0]*(2**bits)
    for ct in ctpairs:
        c0a=ct[0]>>(32*3)
        c1a=(ct[0]>>(32*2))&((1<<32)-1)
        c2a=(ct[0]>>(32*1))&((1<<32)-1)
        #只需用到密文的96bit
        c0b=(ct[1]>>(32*3))&((1<<32)-1)
        c1b=(ct[1]>>(32*2))&((1<<32)-1)
        c2b=(ct[1]>>(32*1))&((1<<32)-1)            

        for key in range(2**bits):
            r1_low_a=(c0a-(left_rotate(c1a^c2a,9)^key))%(2**32)#解密求得目标差分处的值
            r1_low_b=(c0b-(left_rotate(c1b^c2b,9)^key))%(2**32)
            if (r1_low_a&mask)^(r1_low_b&mask)==delta:
                counter[key]+=1
    return counter


import random

cpairs=[]

mainkey=hex(random.randint(0,2**128-1))

keys=gen_key(0x675da180de0bfafae6a055482dc8a135, 7)

c=0

#选择明文对
for i in range(2**12):
    m1=random.randint(0,2**128-1)
    m2=m1^((1<<(26-1))<<(32*3))^(1<<(17-1))
    cpairs.append((ballet_en(m1,keys,7),ballet_en(m2,keys,7)))

bits=14


print("bits=",bits,"outdelta=0b100001000100")

#计数器计数
counter=attack_low_bit(cpairs,0b100001000100,bits)

import json
with open('counter.json','w') as file_p:
    json.dump(counter, file_p)

realkey=left_rotate((keys[6]>>32)^(keys[6]&((1<<32)-1)),9)&((1<<bits)-1)

print(max(counter))#输出最大计数

print(counter[realkey])#输出正确的计数
