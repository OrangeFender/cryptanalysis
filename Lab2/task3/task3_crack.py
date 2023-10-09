   
PC1 = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
]

PC2=[
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

def rotate_left(lst, num_positions):
    if len(lst) == 0:
        return lst

    num_positions %= len(lst)  # 确保num_positions在列表长度范围内

    # 使用切片操作将列表分成两部分，分别进行左移和右移
    left_part = lst[:num_positions]
    right_part = lst[num_positions:]

    # 将两个部分重新组合成一个新列表
    rotated_list = right_part + left_part

    return rotated_list

def int_to_binary_list(num):
    binary_list = [(num >> i) & 1 for i in range(7, -1, -1)]
    return binary_list


result=[]

C=PC1[:28]
D=PC1[28:]

C=rotate_left(C,10)
D=rotate_left(D,10)

CD=C+D

for i in range(48):
    result.append(CD[PC2[i]-1])
    
print(result)

rest=[]
for i in range(56):
    if i not in result:
        rest.append(i+1)

main_key=[0]*56
        
for key in range(256):
    keybits=int_to_binary_list(key)
    for i in range(8):
        main_key[rest[i]-1]=keybits[i]
    for i in range(48):
        main_key[result[i]-1]=subkeybits[i]
        
    for i in range(56):
        