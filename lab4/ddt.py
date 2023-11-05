import numpy as np
DDT0Carryin=np.zeros([65536,256])
DDT1Carryin=np.zeros([65536,256])
DDT2Carryin=np.zeros([65536,256])

for a in range(256):
    for b in range(256):
        for aa in range(256):
            for bb in range(256):
                DDT0Carryin[(a<<8)+b][((aa+bb)%256)^(((a^aa)+(b^bb))%256)]+=1
                DDT1Carryin[(a<<8)+b][((aa+bb+1)%256)^(((a^aa)+(b^bb))%256)]+=1
                DDT2Carryin[(a<<8)+b][((aa+bb+1)%256)^(((a^aa)+(b^bb)+1)%256)]+=1
                
DDTavg=(DDT0Carryin/4+DDT1Carryin/2+DDT2Carryin/4)

file_name = 'DDTavg.txt'
format_options = {
    'delimiter': ' ',    # 使用空格作为分隔符
    'fmt': '%5d',         # 使用空格对齐整数，宽度为5，可根据需要修改宽度
}

# 使用np.savetxt将数组写入文件
np.savetxt(file_name, DDTavg, **format_options)
file_name='DDT0Carryin.txt'
np.savetxt(file_name, DDT0Carryin, **format_options)

np.save('DDTavg.npy', DDTavg)
np.save('DDT0Carryin.npy', DDT0Carryin)
np.save('DDT1Carryin.npy', DDT1Carryin)
np.save('DDT2Carryin.npy', DDT2Carryin)