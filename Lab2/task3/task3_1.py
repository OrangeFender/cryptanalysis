p_permutation_table = [
    16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

inverse_p=[9, 17, 23, 31, 13, 28, 2, 18, 24, 16, 30, 6, 26, 20, 10, 1, 8, 14, 25, 3, 4, 29, 11, 19, 0, 12, 22, 7, 5, 27, 15, 21]

s=[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
    0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
    4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
    15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
   [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
    3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
    0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
    13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
   [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
    13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
    13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
    1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
   [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
    13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
    10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
    3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
   [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
    14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
    4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
    11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
   [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
    10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
    9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
    4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
   [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
    13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
    1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
    6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
   [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
    1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
    7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
    2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

#E扩展，6bit输出
def e_expand(input_block):
    # E扩展表
    e_table = [
        32,  1,  2,  3,  4,  5,
         4,  5,  6,  7,  8,  9,
         8,  9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32,  1
    ]    
    output_block = 0
    for i in range(48):
        # 获取E扩展表中的位索引
        e_bit_index = e_table[i] - 1
        # 获取输入块中对应位的值
        input_bit = (input_block >> (32 - e_bit_index - 1)) & 1
        # 将输入位放置到输出块的相应位置
        output_block = (output_block << 1) | input_bit

    return output_block

def p(input_integer,p_permutation_table):
    output_integer = 0
    for i, bit_position in enumerate(p_permutation_table):
        bit_value = (input_integer >> (32 - bit_position)) & 1
        output_integer |= (bit_value << (31 - i))

    return output_integer

def split_into_4bit_blocks(input_number):
    # 初始化一个空的数组，用于存储4位块
    blocks = [0] * 8

    # 使用位掩码和位移操作来提取每个4位块
    for i in range(8):
        # 计算当前4位块的起始位索引
        start_bit = 28 - (i * 4)
        # 使用位掩码0xF来提取4位块的值
        block_value = (input_number >> start_bit) & 0xF
        # 存储到数组中
        blocks[i] = block_value

    return blocks

def split_into_6bit_blocks(input_number):
    # 初始化一个空的数组，用于存储6位块
    blocks = [0] * 8

    # 使用位掩码和位移操作来提取每个6位块
    for i in range(8):
        # 计算当前6位块的起始位索引
        start_bit = 42 - (i * 6)
        # 使用位掩码0x3F来提取6位块的值
        block_value = (input_number >> start_bit) & 0x3F
        # 存储到数组中
        blocks[i] = block_value

    return blocks

def attacker(delta,ctpair,a):
    a_inv=p(a,inverse_p)
    a_inv_4bit=split_into_4bit_blocks(a_inv)
    
    counter=[[0]*64*64]*4
    
    for key in range(64*64):
        #for i in range(len(ctpair)):
        for i in range(4000):
            l1_inv=p(ctpair[i][0][0],inverse_p)
            l2_inv=p(ctpair[i][1][0],inverse_p)
            #进行逆p置换，方便后续恢复
            l1_inv_4bit=split_into_4bit_blocks(l1_inv)
            l2_inv_4bit=split_into_4bit_blocks(l2_inv)
            r1e=e_expand(ctpair[i][0][1])
            r2e=e_expand(ctpair[i][1][1])
            r1e_6bit=split_into_6bit_blocks(r1e)
            r2e_6bit=split_into_6bit_blocks(r2e)
            for n_of_s in range(4):
                Delta_a_l=(l1_inv_4bit[2*n_of_s]^l2_inv_4bit[2*n_of_s]^a_inv_4bit[2*n_of_s])<<4|l1_inv_4bit[2*n_of_s+1]^l2_inv_4bit[2*n_of_s+1]^a_inv_4bit[2*n_of_s+1]
                D1=(s[2*n_of_s][(r1e_6bit[2*n_of_s]^(key>>6))]^s[2*n_of_s][(r2e_6bit[2*n_of_s]^(key>>6))])<<4|s[2*n_of_s+1][(r1e_6bit[2*n_of_s+1]^(key&0b111111))]^s[2*n_of_s+1][(r2e_6bit[2*n_of_s+1]^(key&0b111111))]#求出D的输出差分
                DeltaB=D1^Delta_a_l
                if DeltaB in delta[n_of_s]:
                    counter[n_of_s][key]=counter[n_of_s][key]+1
            
    return counter


import json

with open('cipher_pair_list.json', 'r') as file:
    cipher_pair_list = json.load(file)


a=0x04000000

Delta=[[]]*4

Delta[0]=[3*4]#由s1分布表得

Delta[1]=[0b10100101,0b10100110,0b10101001,0b10101010]
Delta[2]=[0]
Delta[3]=[0]

counter=attacker(Delta,cipher_pair_list,a)

print(counter)
print("-----------------------------------------")
for i in range(len(counter)):
    print(sorted(counter[i]))
    print("-----------------------------------------")