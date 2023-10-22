def generate_binary_strings(binary_str):
    results = []

    def generate_helper(current_str, index):
        if index == len(binary_str):
            results.append(current_str)
            return
        if binary_str[index] == '*':
            generate_helper(current_str + '0', index + 1)
            generate_helper(current_str + '1', index + 1)
        else:
            generate_helper(current_str + binary_str[index], index + 1)

    generate_helper('', 0)
    return results

binary_str = "1*0*"
combinations = generate_binary_strings(binary_str)
for combo in combinations:
    print(combo)

subkeys=generate_binary_strings("0*101*****1*110****1010*1*1*0000***1")

with open("keys.txt", "w") as file:
    for key in subkeys:
        file.write(key + "\n")
        
        