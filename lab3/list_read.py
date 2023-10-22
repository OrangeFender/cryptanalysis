import json

with open('plain_list.json','w') as file_p:
    plain_list = json.load(file_p)

with open('cipher_list.json','w') as file_c:
    cipher_list = json.load(file_c)

for item in plain_list:
    print(item)

for item in cipher_list:
    print(item)