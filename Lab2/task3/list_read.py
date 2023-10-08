import json

with open('cipher_pair_list.json', 'r') as file:
    cipher_pair_list = json.load(file)

#cipher_pair_list就是25600个元素的列表，每个元素是[(cipher_l,cipher_r),(cipher_friend_l,cipher_friend_r)]

#print(cipher_pair_list)

for item in cipher_pair_list:
    print(item)