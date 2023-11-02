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


def ballet_de(ciphertext, key, round_):
    n = 1 << 32
    mask = n - 1
    x = []
    ne = [0] * 4
    for i in range(3, -1, -1):
        x.append(ciphertext >> (32 * i) & mask)
    # r - 1 轮解密
    for i in range(round_ - 1):
        skl = key[i] >> 32 & mask
        skr = key[i] & mask
        ne[0] = x[1] ^ skl
        ne[1] = right_rotate(((x[0] - left_rotate(x[1] ^ x[2] ^ skl ^ skr, 9)) % n), 6)
        ne[2] = right_rotate(((x[3] - left_rotate(x[1] ^ x[2] ^ skl ^ skr, 14)) % n), 15)
        ne[3] = x[2] ^ skr
        for i in range(4):
            x[i] = ne[i]
    # 第r轮解密
    skl = key[round_ - 1] >> 32 & mask
    skr = key[round_ - 1] & mask
    ne[0] = right_rotate(((x[0] - left_rotate(x[1] ^ x[2] ^ skl ^ skr, 9)) % n), 6)
    ne[1] = x[1] ^ skl
    ne[2] = x[2] ^ skr
    ne[3] = right_rotate(((x[3] - left_rotate(x[1] ^ x[2] ^ skl ^ skr, 14)) % n), 15)

    plaintext = 0
    for i in range(4):
        plaintext <<= 32
        plaintext += ne[i]

    return plaintext





