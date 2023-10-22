import random
import subprocess
import json

def split_string(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

plain_list=[]
cipher_list=[]
for i in range(30000):
    print(i)
    #随机生成明文对
    input_data=random.randint(0,2**64-1)
    high_32_bits = (input_data >> 32) & 0xFFFFFFFF
    low_32_bits = input_data & 0xFFFFFFFF 
    plain=(high_32_bits, low_32_bits)
    plain_list.append(plain)

    #将数字明文转换成字符串明文，以16进制表示，共有16个16进制数(4bit)，总共64bit
    input_hex = hex(input_data)[2:].rjust(16,'0')

    #每2个16进制作为1组，共8组
    plain_text = split_string(input_hex, 2)

    #执行加密程序
    command=['./des_enc1',plain_text[0], plain_text[1], plain_text[2], plain_text[3], plain_text[4], plain_text[5], plain_text[6], plain_text[7]]
    cipher = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)

    #构造存储单元
    cipher_l=int(cipher[:8],16)
    cipher_r=int(cipher[8:],16)
    cipher=(cipher_l, cipher_r)

    cipher_list.append(cipher)
    
#保存list对象，用于协同工作
with open('plain_list.json','w') as file_p:
    json.dump(plain_list, file_p)

with open('cipher_list.json','w') as file_c:
    json.dump(cipher_list, file_c)
