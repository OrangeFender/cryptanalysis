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

def p(input_integer,p_permutation_table):
    output_integer = 0
    for i, bit_position in enumerate(p_permutation_table):
        bit_value = (input_integer >> (32 - bit_position)) & 1
        output_integer |= (bit_value << (31 - i))

    return output_integer

x=[0x0a000000,0x00000600]
for input in x:
    print(hex(p(input,p_permutation_table)))
    