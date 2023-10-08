import random
import subprocess
import json

def split_string(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

cipher_pair_list=[]
for i in range(25600):
    print(i)
    #随机生成明文对
    input_data=random.randint(0,2**64-1)
    diff=0x4008000004000000
    input_data_friend=input_data^diff

    #将数字明文转换成字符串明文，以16进制表示，共有16个16进制数(4bit)，总共64bit
    input_hex = hex(input_data)[2:].rjust(16,'0')
    input_friend_hex = hex(input_data_friend)[2:].rjust(16,'0')

    #每2个16进制作为1组，共8组
    plain_text = split_string(input_hex, 2)
    plain_text_friend = split_string(input_friend_hex, 2)

    #执行加密程序
    command=['./des_enc1',plain_text[0], plain_text[1], plain_text[2], plain_text[3], plain_text[4], plain_text[5], plain_text[6], plain_text[7]]
    command_friend=['./des_enc1',plain_text_friend[0], plain_text_friend[1], plain_text_friend[2], plain_text_friend[3], plain_text_friend[4], plain_text_friend[5], plain_text_friend[6], plain_text_friend[7]]
    cipher = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
    cipher_friend = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
    
    #构造存储单元
    cipher_l=int(cipher[:8],16)
    cipher_r=int(cipher[8:],16)
    cipher=(cipher_l, cipher_r)

    cipher_friend_l=int(cipher_friend[:8],16)
    cipher_friend_r=int(cipher_friend[8:],16)
    cipher_friend=(cipher_friend_l, cipher_friend_r)
    
    cipher_pair=(cipher, cipher_friend)
    cipher_pair_list.append(cipher_pair)

#保存list对象，用于协同工作
with open('cipher_pair_list.json','w') as file:
    json.dump(cipher_pair_list, file)
