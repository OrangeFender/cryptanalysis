
PC1 = [57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4]

PC2 = [14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

shift = [ 1,  1,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  1]

def mainkey(key):
    # initial key schedule calculation
    choice1, choice2 = [0]*56, [0]*48
    for i in range(56):
        choice1[i] = key[PC1[i]-1]

    C = choice1[:28]
    D = choice1[28:]

    subkey = []

    for i in range(16):
        C = C[shift[i]:] + C[:shift[i]]
        D = D[shift[i]:] + D[:shift[i]]

        temp = C + D
        for i in range(48):
            choice2[i] = temp[PC2[i]-1]

        subkey.append(choice2)
        choice2 = [0]*48

    return subkey

key = 0x82793e7900000000
kk = bin(key)[2:]
kk = list(kk[:32]) + ['*']*32
subkey = mainkey(kk)




    

    

