from collections import OrderedDict

def remove_duplicates(input_file, output_file):
    lines = []
    
    # 读取文件并去除重复行
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line not in lines:
                lines.append(line)
    
    # 将去重后的行写入输出文件，保持原文顺序
    with open(output_file, 'w') as file:
        for line in lines:
            file.write(line + '\n')

if __name__ == "__main__":
    input_file_path = "key_step2.txt"
    output_file_path = "key_step3.txt"
    
    remove_duplicates(input_file_path, output_file_path)
    print("重复行已去除，结果保存在key_step3.txt文件中。")
