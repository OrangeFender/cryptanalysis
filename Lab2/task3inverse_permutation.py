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
def inverse_permutation(perm):
    n = len(perm)
    inverse_perm = [0] * n
    
    for i in range(n):
        inverse_perm[perm[i-1]-1] = i
    
    return inverse_perm

def p(input_integer,p_permutation_table):
    output_integer = 0
    for i, bit_position in enumerate(p_permutation_table):
        bit_value = (input_integer >> (32 - bit_position)) & 1
        output_integer |= (bit_value << (31 - i))

    return output_integer


a=0xABCDEF12

a=p(a,p_permutation_table)
a=p(a,inverse_permutation(p_permutation_table))
print(hex(a))

print(inverse_permutation(p_permutation_table))